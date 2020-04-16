from typing import List, Union, Optional, Tuple
import datetime
from db_session import Session
from model import *
from sqlalchemy.sql import func
import re
import json
import sys
import os
import yaml
import pharmacy
import impl
import rcpt


class Presc:
    def __init__(self, visit, presc_content, fax):
        self.visit = visit
        self.presc_content = presc_content
        self.fax = fax


def ensure_sqldate(at: Union[str, datetime.datetime, datetime.date]) -> str:
    if isinstance(at, str):
        n = len(at)
        if n == 10:
            return at
        elif n < 10:
            raise Exception(f"Invalid at: {at}")
        else:
            return at[:10]
    elif isinstance(at, datetime.datetime) or isinstance(at, datetime.date):
        return at.strftime("%Y-%m-%d")
    else:
        raise Exception(f"Cannot normalize at: {at}")


def list_visit(session, date_from, date_upto) -> List[Visit]:
    dfrom = ensure_sqldate(date_from)
    dupto = ensure_sqldate(date_upto)
    return (session.query(Visit).filter(func.date(Visit.visited_at) >= dfrom)
            .filter(func.date(Visit.visited_at) <= dupto)
            .order_by(Visit.visit_id)
            .all())


def list_text(session, visit_id) -> List[Text]:
    return session.query(Text).filter(Text.visit_id == visit_id).order_by(Text.text_id).all()


re_presc_marker = re.compile(r"院外処方.*\n")


def probe_presc_text(content: str) -> Optional[str]:
    t = content.strip()
    if re_presc_marker.match(t):
        return re.sub(re_presc_marker, "", t, 1)
    else:
        return None


re_pharma_marker = re.compile(r"(.+)にファックス（(\+\d+)）で")
re_presc_hand_over = re.compile(r"処方箋を渡した")
re_presc_physical_mail = re.compile(r"自宅に処方箋を郵送")
re_presc_mail = re.compile(r"(電子)?メールで処方箋を送付した")
re_presc_home = re.compile(r"処方箋を自宅にファックスで送った")


def probe_pharma(content: str) -> Optional[Tuple[str, str]]:
    m = re_pharma_marker.match(content)
    if m:
        return m.group(1), m.group(2)
    else:
        return None


def probe_presc_hand_over(content: str) -> bool:
    return re_presc_hand_over.match(content) is not None


def probe_presc_mail(content: str) -> bool:
    return re_presc_mail.match(content) is not None


def probe_presc_home(content: str) -> bool:
    return re_presc_home.match(content) is not None


def probe_presc_physical_mail(content: str) -> bool:
    return re_presc_physical_mail.match(content) is not None


def compose_hihokensha(shahokokuho):
    def cvt_to_str(value):
        if value is None:
            return ""
        else:
            return str(value)
    kigou = cvt_to_str(shahokokuho.hihokensha_kigou)
    bangou = cvt_to_str(shahokokuho.hihokensha_bangou)
    if kigou and bangou:
        return kigou + " ・ " + bangou
    elif kigou:
        return kigou
    elif bangou:
        return bangou
    else:
        return ""


def set_shohousen_hoken(shohousen, hoken) -> None:
    if hoken.shahokokuho:
        shahokokuho = hoken.shahokokuho
        shohousen["hokenshaBangou"] = str(shahokokuho.hokensha_bangou)
        shohousen["hihokensha"] = compose_hihokensha(shahokokuho)
        shohousen["honnin"] = shahokokuho.honnin != 0
    elif hoken.koukikourei:
        shohousen["hokenshaBangou"] = str(hoken.koukikourei.hokensha_bangou)
        shohousen["hihokensha"] = str(hoken.koukikourei.hihokensha_bangou)
    kouhi_list = [kouhi for kouhi in [hoken.kouhi_1, hoken.kouhi_2, hoken.kouhi_3] if kouhi]
    if len(kouhi_list) > 0:
        kouhi_1 = kouhi_list[0]
        shohousen["futansha"] = str(kouhi_1.futansha)
        shohousen["jukyuysga"] = str(kouhi_1.jukyuusha)
        if len(kouhi_list) > 1:
            kouhi_2 = kouhi_list[1]
            shohousen["futansha2"] = str(kouhi_2.futansha)
            shohousen["jukyuysga2"] = str(kouhi_2.jukyuusha)


def set_shohousen_patient(session, shohousen, patient) -> None:
    shohousen["shimei"] = patient.last_name + patient.first_name
    shohousen["birthday"] = ensure_sqldate(patient.birthday)
    shohousen["sex"] = patient.sex


def to_shohousen(session, presc):
    shohousen = {
        "visit_id": presc.visit.visit_id
    }
    hoken = impl.get_hoken(session, presc.visit.visit_id)
    patient = impl.get_patient(session, presc.visit.patient_id)
    rcpt_age = rcpt.calc_rcpt_age_by_date(patient.birthday, presc.visit.visited_at.date())
    futan_wari = rcpt.calc_futan_wari(hoken, rcpt_age)
    set_shohousen_hoken(shohousen, hoken)
    set_shohousen_patient(session, shohousen, patient)
    shohousen["futanWari"] = futan_wari
    shohousen["koufuDate"] = ensure_sqldate(presc.visit.visited_at.date())
    shohousen["content"] = presc.presc_content
    shohousen["pharmacy_fax"] = presc.fax
    return shohousen


def list_presc(session, from_date, upto_date) -> List[Presc]:
    visits = list_visit(session, from_date, upto_date)
    result: List[Presc] = []
    for v in visits:
        texts = list_text(session, v.visit_id)
        presc_hit = False
        presc = None
        pharma = None
        hand_over = False
        mail = False
        fax_home = False
        physical_mail = False
        for t in texts:
            opt_presc = probe_presc_text(t.content)
            if opt_presc:
                if presc:
                    raise Exception(f"multiple presc: {v}")
                presc = t.content
                presc_hit = True
            elif presc_hit:
                opt_pharma = probe_pharma(t.content)
                if opt_pharma:
                    pharma = opt_pharma
                elif probe_presc_hand_over(t.content):
                    hand_over = True
                elif probe_presc_mail(t.content):
                    mail = True
                elif probe_presc_home(t.content):
                    fax_home = True
                elif probe_presc_physical_mail(t.content):
                    physical_mail = True
                presc_hit = False
        if presc:
            if pharma:
                _, fax = pharma
                result.append(Presc(v, presc, fax))
            elif hand_over or mail or fax_home or physical_mail:
                pass
            else:
                raise Exception(f"presc without pharma {v}")
    return result


def get_pharmacy_list():
    return [p.to_dict() for p in pharmacy.get_pharmacy_list()]


def get_clinic_info():
    conf = impl.CLINIC_INFO
    return {
        "clinicAddress": conf["postalCode"] + " " + conf["address"],
        "clinicName": conf["name"],
        "clinicPhone": "電話 " + conf["tel"],
        "kikancode": str(conf["todoufukencode"]) + str(conf["tensuuhyoucode"]) + str(conf["kikancode"]),
        "doctorName": conf["doctorName"]
    }


def run(from_date, upto_date):
    session = Session()
    presc_list = list_presc(session, from_date, upto_date)
    result = {
        "clinicInfo": get_clinic_info(),
        "pharmacies": get_pharmacy_list(),
        "shohousen": [to_shohousen(session, presc) for presc in presc_list]
    }
    print(json.dumps(result, indent=4, ensure_ascii=False))
    session.close()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        run(sys.argv[1], sys.argv[2])
    else:
        print("Usage: presc date_from date_upto", file=sys.stderr)


