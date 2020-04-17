from typing import List, Union, Optional, Tuple
import datetime
from db_session import Session
from model import *
from sqlalchemy.sql import func
import re
import json
import sys
import pharmacy
import impl
import rcpt
import argparse
import codecs


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


def run_data(date_from, date_upto, output=None):
    session = Session()
    presc_list = list_presc(session, date_from, date_upto)
    result = {
        "date_from": date_from,
        "date_upto": date_upto,
        "clinicInfo": get_clinic_info(),
        "pharmacies": get_pharmacy_list(),
        "shohousen": [to_shohousen(session, presc) for presc in presc_list]
    }
    data = json.dumps(result, indent=4, ensure_ascii=False)
    if output:
        with open(output, "w", encoding="UTF-8") as fs:
            fs.write(data)
    else:
        print(data)
    session.close()


def run_print(input_file=None, output=None):
    if input_file:
        with open(input_file, "r", encoding="UTF-8") as fp:
            data = json.load(fp)
    else:
        data = json.load(sys.stdin)
    clinic_info = data["clinicInfo"]

    def to_presc(item):
        p = dict(clinic_info)
        for key in ["hokenshaBangou", "hihokensha", "futansha", "jukyuusha", "futansha2", "jukyuusha2",
                    "shimei", "birthday", "sex", "honnin", "futanWari", "koufuDate", "validUptoDate", "content"]:
            if key in item:
                p[key] = item[key]
        return p

    plist = [to_presc(p) for p in data["shohousen"]]
    result = json.dumps(plist, indent=4, ensure_ascii=False)
    if output:
        with open(output, "w", encoding="UTF-8") as fs:
            fs.write(result)
    else:
        print(result)


def run():
    parser = argparse.ArgumentParser(description="Processes prescripton")
    sub_parsers = parser.add_subparsers()
    parser_data = sub_parsers.add_parser("data")
    parser_data.add_argument("date_from", metavar="DATE-FROM")
    parser_data.add_argument("date_upto", metavar="DATE-UPTO")
    parser_data.add_argument("-o", "--output")
    parser_data.set_defaults(func=run_data)
    parser_print = sub_parsers.add_parser("print")
    parser_print.add_argument("-i", "--input", dest="input_file")
    parser_print.add_argument("-o", "--output")
    parser_print.set_defaults(func=run_print)
    args = parser.parse_args()
    f = args.func
    kwargs = vars(args)
    del kwargs["func"]
    f(**kwargs)


if __name__ == "__main__":
    run()


