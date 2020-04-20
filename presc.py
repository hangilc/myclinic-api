from typing import List, Union, Optional, Tuple, Dict
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
from functools import reduce
import operator
import datetime
from pharmacy import Pharmacy


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


def ensure_date(d: Union[str, datetime.datetime, datetime.date]) -> datetime.date:
    if isinstance(d, str):
        return datetime.datetime.strptime(d, "%Y-%m-%d").date()
    elif isinstance(d, datetime.date):
        return d
    elif isinstance(d, datetime.datetime):
        return d.date()
    else:
        raise Exception(f"cannot convert to date: {d}")


class ShohousenClinicInfo:
    def __init__(self, address, name, phone, kikancode, doctor_name):
        self.address = address
        self.name = name
        self.phone = phone
        self.kikancode = kikancode
        self.doctor_name = doctor_name

    @classmethod
    def from_clinic_info(cls, clinic_info: ClinicInfo):
        c = clinic_info
        return cls(
            c.postal_code + " " + c.address,
            c.name,
            "電話 " + c.tel,
            str(c.todoufukencode) + str(c.tensuuhyoucode) + str(c.kikancode),
            c.doctor_name
        )

    def to_dict(self):
        return {
            "clinicAddress": self.address,
            "clinicName": self.name,
            "clinicPhone": self.phone,
            "kikancode": self.kikancode,
            "doctorName": self.doctor_name
        }


def get_clinic_info():
    conf = dict(impl.get_clinic_info())
    conf["todoufukencode"] = format(conf["todoufukencode"], "02d")
    conf["tensuuhyoucode"] = str(conf["tensuuhyoucode"])
    conf["kikancode"] = str(conf["kikancode"])
    clinic_info = ClinicInfo.from_dict(conf)
    return ShohousenClinicInfo.from_clinic_info(clinic_info)
    # return {
    #     "clinicAddress": conf["postalCode"] + " " + conf["address"],
    #     "clinicName": conf["name"],
    #     "clinicPhone": "電話 " + conf["tel"],
    #     "kikancode": str(conf["todoufukencode"]) + str(conf["tensuuhyoucode"]) + str(conf["kikancode"]),
    #     "doctorName": conf["doctorName"]
    # }


class Presc:
    def __init__(self, visit: Visit, presc_content: str, fax: str):
        self.visit = visit
        self.presc_content = presc_content
        self.fax = fax

    def to_dict(self) -> Dict:
        return {
            "visit": self.visit.to_dict(),
            "presc_content": self.presc_content,
            "fax": self.fax
        }


class ShohousenGroup:
    def __init__(self, pharmacy_arg: Pharmacy, items: List[Presc]):
        self.pharmacy = pharmacy_arg
        self.items = items

    def to_dict(self):
        return {
            "pharmacy": self.pharmacy.to_dict(),
            "items": [item.to_dict() for item in self.items]
        }


class ShohousenBundle:
    def __init__(self, date_from: datetime.date, date_upto: datetime.date, clinic_info: ShohousenClinicInfo,
                 groups: List[ShohousenGroup]):
        self.date_from = date_from
        self.date_upto = date_upto
        self.clinic_info = clinic_info
        self.groups = groups

    def to_dict(self):
        return {
            "date_from": ensure_sqldate(self.date_from),
            "date_upto": ensure_sqldate(self.date_upto),
            "clinic_info": self.clinic_info.to_dict(),
            "groups": [g.to_dict() for g in self.groups]
        }


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


def get_pharmacy_list() -> List[Pharmacy]:
    return pharmacy.get_pharmacy_list()


def do_output(value: str, dest: Optional[str]) -> None:
    if dest:
        with open(dest, "w", encoding="UTF-8") as fs:
            fs.write(value)
    else:
        print(value)


def run_data(date_from, date_upto, output=None):
    session = Session()
    pharmacies: List[Pharmacy] = get_pharmacy_list()
    pharma_map: Dict[str, Pharmacy] = {p.fax: p for p in pharmacies}
    presc_list: List[Presc] = list_presc(session, date_from, date_upto)
    presc_groups: Dict[str, ShohousenGroup] = {}
    for item in presc_list:
        fax = item.fax
        if fax not in presc_groups:
            pharma = pharma_map[fax]
            presc_groups[fax] = ShohousenGroup(pharma, [])
        presc_groups[fax].items.append(item)
    ordered_presc_groups: List[Tuple[str, ShohousenGroup]] = [(sg.pharmacy.fax, sg) for sg in presc_groups.values()]
    ordered_presc_groups.sort(key=lambda x: len(x[1].items), reverse=True)
    data = ShohousenBundle(ensure_date(date_from), ensure_date(date_upto), get_clinic_info(),
                           [sg for fax, sg in ordered_presc_groups])
    json_rep = json.dumps(data.to_dict(), indent=2, ensure_ascii=False)
    do_output(json_rep, output)
    session.close()


def make_pharma_map(pharma_list):
    return {
        p["fax"]: p for p in pharma_list
    }


def run_print(input_file=None, output=None):
    if input_file:
        with open(input_file, "r", encoding="UTF-8") as fp:
            data = json.load(fp)
    else:
        data = json.load(sys.stdin)
    clinic_info = data["clinicInfo"]
    pharma_map = make_pharma_map(data["pharmacies"])
    presc_groups = {}
    for item in data["shohousen"]:
        fax = item["pharmacy_fax"]
        if fax not in presc_groups:
            presc_groups[fax] = []
        presc_groups[fax].append(item)
    ordered_presc_groups = [(fax, ps) for fax, ps in presc_groups.items()]
    ordered_presc_groups.sort(key=lambda item: len(item[1]), reverse=True)
    for g in ordered_presc_groups:
        print(pharma_map[g[0]]["name"], len(g[1]), file=sys.stderr)

    def to_presc(presc_item):
        p = dict(clinic_info)
        for key in ["hokenshaBangou", "hihokensha", "futansha", "jukyuusha", "futansha2", "jukyuusha2",
                    "shimei", "birthday", "sex", "honnin", "futanWari", "koufuDate", "validUptoDate", "content"]:
            if key in presc_item:
                p[key] = presc_item[key]
        p["pharmacyName"] = pharma_map[presc_item["pharmacy_fax"]]["name"]
        return p

    plist = [to_presc(p) for p in reduce(operator.add, (ps_item for _, ps_item in ordered_presc_groups))]
    result = json.dumps(plist, indent=4, ensure_ascii=False)
    if output:
        with open(output, "w", encoding="UTF-8") as fs:
            fs.write(result)
    else:
        print(result)


def run():
    parser = argparse.ArgumentParser(description="Processes prescripton")
    sub_parsers = parser.add_subparsers()
    # data
    parser_data = sub_parsers.add_parser("data")
    parser_data.add_argument("date_from", metavar="DATE-FROM")
    parser_data.add_argument("date_upto", metavar="DATE-UPTO")
    parser_data.add_argument("-o", "--output")
    parser_data.set_defaults(func=run_data)
    # print
    parser_print = sub_parsers.add_parser("print")
    parser_print.add_argument("-i", "--input", dest="input_file")
    parser_print.add_argument("-o", "--output")
    parser_print.set_defaults(func=run_print)
    #
    args = parser.parse_args()
    f = args.func
    kwargs = vars(args)
    del kwargs["func"]
    f(**kwargs)


if __name__ == "__main__":
    run()


