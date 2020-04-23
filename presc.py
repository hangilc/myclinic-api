import io
from typing import List, Union, Optional, Tuple, Dict

import kanjidate
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
import datetime
from pharmacy import Pharmacy
import os
import glob
from jinja2 import Environment, FileSystemLoader


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
        if len(d) > 10:
            d = d[:10]
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
            "address": self.address,
            "name": self.name,
            "phone": self.phone,
            "kikancode": self.kikancode,
            "doctor_name": self.doctor_name
        }

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            d["address"],
            d["name"],
            d["phone"],
            d["kikancode"],
            d["doctor_name"]
        )


def get_clinic_info():
    conf = dict(impl.get_clinic_info())
    conf["todoufukencode"] = format(conf["todoufukencode"], "02d")
    conf["tensuuhyoucode"] = str(conf["tensuuhyoucode"])
    conf["kikancode"] = str(conf["kikancode"])
    clinic_info = ClinicInfo.from_dict(conf)
    return ShohousenClinicInfo.from_clinic_info(clinic_info)


class Presc:
    def __init__(self, visit: Visit, presc_content: str, fax: str,
                 hoken: Hoken, patient: Patient):
        self.visit = visit
        self.presc_content = presc_content
        self.fax = fax
        self.hoken = hoken
        self.patient = patient

    def to_dict(self) -> Dict:
        return {
            "visit": self.visit.to_dict(),
            "presc_content": self.presc_content,
            "fax": self.fax,
            "hoken": self.hoken.to_dict(),
            "patient": self.patient.to_dict()
        }

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            Visit.from_dict(d["visit"]),
            d["presc_content"],
            d["fax"],
            Hoken.from_dict(d["hoken"]),
            Patient.from_dict(d["patient"])
        )


class ShohousenGroup:
    def __init__(self, pharmacy_arg: Pharmacy, items: List[Presc]):
        self.pharmacy = pharmacy_arg
        self.items = items

    def to_dict(self):
        return {
            "pharmacy": self.pharmacy.to_dict(),
            "items": [item.to_dict() for item in self.items]
        }

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(Pharmacy.from_dict(
            d["pharmacy"]),
            [Presc.from_dict(x) for x in d["items"]]
        )


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

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            ensure_date(d["date_from"]),
            ensure_date(d["date_upto"]),
            ShohousenClinicInfo.from_dict(d["clinic_info"]),
            [ShohousenGroup.from_dict(x) for x in d["groups"]]
        )


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


class Shohousen:
    def __init__(self, hokensha_bangou="", hihokensha="", futansha="", jukyuusha="",
                 futansha2="", jukyuusha2="", shimei="", birthday: Optional[datetime.date] = None,
                 sex: Optional[str] = None, honnin: Optional[bool] = None,
                 futan_wari: Optional[int] = None, koufu_date: Optional[datetime.date] = None,
                 content="", pharmacy_name=""):
        self.hokensha_bangou = hokensha_bangou
        self.hihokensha = hihokensha
        self.futansha = futansha
        self.jukyuusha = jukyuusha
        self.futansha2 = futansha2
        self.jukyuusha2 = jukyuusha2
        self.shimei = shimei
        self.birthday = birthday
        self.sex = sex
        self.honnin = honnin
        self.futan_wari = futan_wari
        self.koufu_date = koufu_date
        self.content = content
        self.pharmacy_name = pharmacy_name

    def set_hoken(self, hoken: Hoken) -> None:
        if hoken.shahokokuho:
            shahokokuho = hoken.shahokokuho
            self.hokensha_bangou = str(shahokokuho.hokensha_bangou)
            self.hihokensha = compose_hihokensha(shahokokuho)
            self.honnin = shahokokuho.honnin != 0
        elif hoken.koukikourei:
            self.hokensha_bangou = str(hoken.koukikourei.hokensha_bangou)
            self.hihokensha = str(hoken.koukikourei.hihokensha_bangou)
        kouhi_list = [kouhi for kouhi in [hoken.kouhi_1, hoken.kouhi_2, hoken.kouhi_3] if kouhi]
        if len(kouhi_list) > 0:
            kouhi_1 = kouhi_list[0]
            self.futansha = str(kouhi_1.futansha)
            self.jukyuusha = str(kouhi_1.jukyuusha)
            if len(kouhi_list) > 1:
                kouhi_2 = kouhi_list[1]
                self.futansha2 = str(kouhi_2.futansha)
                self.jukyuusha = str(kouhi_2.jukyuusha)

    def set_patient(self, patient: Patient) -> None:
        self.shimei = patient.last_name + patient.first_name
        self.birthday = ensure_sqldate(patient.birthday)
        self.sex = patient.sex

    @classmethod
    def from_presc(cls, presc: Presc, pharmacy_name: str):
        shohousen = cls()
        hoken = presc.hoken
        shohousen.set_hoken(hoken)
        patient = presc.patient
        shohousen.set_patient(patient)
        birthday = ensure_date(patient.birthday)
        visit_day = ensure_date(presc.visit.visited_at)
        rcpt_age = rcpt.calc_rcpt_age_by_date(birthday, visit_day)
        shohousen.futan_wari = rcpt.calc_futan_wari(hoken, rcpt_age)
        shohousen.koufu_date = ensure_date(presc.visit.visited_at)
        shohousen.content = presc.presc_content
        shohousen.pharmacy_name = pharmacy_name
        return shohousen

    def to_input(self, clinic_info: ShohousenClinicInfo) -> Dict:
        return {
            "clinicAddress": clinic_info.address,
            "clinicName": clinic_info.name,
            "clinicPhone": clinic_info.phone,
            "kikancode": clinic_info.kikancode,
            "doctorName": clinic_info.doctor_name,
            "hokenshaBangou": self.hokensha_bangou,
            "hihokensha": self.hihokensha,
            "futansha": self.futansha,
            "jukyuusha": self.jukyuusha,
            "futansha2": self.futansha2,
            "jukyuusha2": self.jukyuusha2,
            "shimei": self.shimei,
            "birthday": ensure_sqldate(self.birthday) if self.birthday else None,
            "sex": self.sex,
            "honnin": self.honnin,
            "futanWari": self.futan_wari,
            "koufuDate": ensure_sqldate(self.koufu_date) if self.koufu_date else None,
            "content": self.content,
            "pharmacyName": self.pharmacy_name
        }


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
                result.append(Presc(v, presc, fax,
                                    impl.get_hoken(session, v.visit_id),
                                    impl.get_patient(session, v.patient_id)))
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


def do_input(input_file: Optional[str]) -> Dict:
    if input_file:
        with open(input_file, "r", encoding="UTF-8") as fp:
            return json.load(fp)
    else:
        return json.load(sys.stdin)


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


def run_print(input_file=None, output=None):
    dict_data = do_input(input_file)
    bundle: ShohousenBundle = ShohousenBundle.from_dict(dict_data)
    shohousen_list: List[Shohousen] = []
    for group in bundle.groups:
        pharma_name = group.pharmacy.name
        shohousen_list += [Shohousen.from_presc(item, pharma_name) for item in group.items]
    json_rep = json.dumps([s.to_input(bundle.clinic_info) for s in shohousen_list], indent=2, ensure_ascii=False)
    do_output(json_rep, output)


def run_print_blank(output=None):
    shohousen = Shohousen()
    json_rep = json.dumps([shohousen.to_input(get_clinic_info())], indent=2, ensure_ascii=False)
    do_output(json_rep, output)


def run_comparison(input_file=None, output=None, directory="."):
    dict_data = do_input(input_file)
    bundle: ShohousenBundle = ShohousenBundle.from_dict(dict_data)
    specs = []
    for g in bundle.groups:
        for item in g.items:
            patient = item.patient
            visit_day = ensure_date(item.visit.visited_at)
            stamp = visit_day.strftime("%Y%m%d")
            needle = f"*-{patient.patient_id}-{stamp}-stamped*.pdf"
            found = glob.glob(os.path.join(directory, needle))
            if len(found) == 0:
                print(f"Cannot find faxed pdf for patient {patient.last_name}{patient.first_name} at {visit_day}")
            src = found[0]
            src = src.replace("\\", "/")
            specs.append({
                "src": src,
                "name": f"{patient.last_name}{patient.first_name}",
                "pharma": g.pharmacy.name
            })
    env = Environment(loader=FileSystemLoader("./t"
                                              "emplates", encoding="utf-8"))
    tmpl = env.get_template("shohousen-comparison.html.jinja2")
    html = tmpl.render({"data": specs})
    do_output(html, output)


def run_pharma_letter(input_file=None, output=None):
    dict_data = do_input(input_file)
    bundle: ShohousenBundle = ShohousenBundle.from_dict(dict_data)

    def render_date(d: datetime.date) -> str:
        geng, nen = kanjidate.date_to_gengou(d)
        return f"{geng}{nen}年{d.month}月{d.day}日"

    date_from_rep = render_date(bundle.date_from)
    date_upto_rep = render_date(bundle.date_upto)
    clinic_info = bundle.clinic_info

    def render_page(g) -> str:
        out = io.StringIO()
        print(g.pharmacy.name, file=out)
        print("担当者様", file=out)
        print("", file=out)
        print(f"{date_from_rep}から{date_upto_rep}までに当院からファックスした処方箋の原本です。", file=out)
        print("", file=out)
        for item in g.items:
            name = item.patient.last_name + item.patient.first_name
            visit_date_rep = render_date(ensure_date(item.visit.visited_at))
            print(f"{name}　{visit_date_rep}", file=out)
        print("", file=out)
        print(clinic_info.address, file=out)
        print(clinic_info.phone, file=out)
        print(clinic_info.name, file=out)
        print(clinic_info.doctor_name, file=out)
        return out.getvalue()

    pages = [render_page(g) for g in bundle.groups]
    rep = "{{ new-page }}\n".join(pages)
    do_output(rep, output)


def run_pharma_label(input_file=None, output=None) -> None:
    dict_data = do_input(input_file)
    bundle: ShohousenBundle = ShohousenBundle.from_dict(dict_data)
    content = []
    data = {"labels": content}
    addr_map = pharmacy.pharma_addr_map
    for g in bundle.groups:
        pharma = g.pharmacy
        lines = addr_map[pharma.fax].split("\n")
        content.append(lines)
    json_rep = json.dumps(data, indent=2, ensure_ascii=False)
    do_output(json_rep, output)


def run_pharma_addr(input_file=None, output=None) -> None:
    dict_data = do_input(input_file)
    bundle: ShohousenBundle = ShohousenBundle.from_dict(dict_data)
    data = {}
    for g in bundle.groups:
        pharma = g.pharmacy
        postal_code = "〒" + pharma.addr[0]
        addr = pharma.addr[1].replace("東京都", "").strip()
        data[pharma.fax] = f"{postal_code}\n{addr}\n{pharma.name} 御中"
    json_rep = json.dumps(data, indent=2, ensure_ascii=False)
    do_output(json_rep, output)


def run_clinic_label(count=1, output=None) -> None:
    clinic_info = impl.get_clinic_info()
    content = []
    data = {"labels": content}
    lines = [
        clinic_info["postalCode"],
        clinic_info["address"],
        clinic_info["name"]
    ]
    for _ in range(count):
        content.append(lines)
    json_rep = json.dumps(data, indent=2, ensure_ascii=False)
    do_output(json_rep, output)


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
    # print-blank
    parser_print_blank = sub_parsers.add_parser("print-blank")
    parser_print_blank.add_argument("-o", "--output")
    parser_print_blank.set_defaults(func=run_print_blank)
    # comparison
    parser_comparison = sub_parsers.add_parser("comparison")
    parser_comparison.add_argument("-i", "--input", dest="input_file")
    parser_comparison.add_argument("-d", "--directory", help="shohousen (fax) directory")
    parser_comparison.add_argument("-o", "--output")
    parser_comparison.set_defaults(func=run_comparison)
    # pharma-letter
    parser_pharma_letter = sub_parsers.add_parser("pharma-letter")
    parser_pharma_letter.add_argument("-i", "--input", dest="input_file")
    parser_pharma_letter.add_argument("-o", "--output")
    parser_pharma_letter.set_defaults(func=run_pharma_letter)
    # pharma-label
    parser_pharma_label = sub_parsers.add_parser("pharma-label")
    parser_pharma_label.add_argument("-i", "--input", dest="input_file")
    parser_pharma_label.add_argument("-o", "--output")
    parser_pharma_label.set_defaults(func=run_pharma_label)
    # pharma-addr
    parser_pharma_addr = sub_parsers.add_parser("pharma-addr")
    parser_pharma_addr.add_argument("-i", "--input", dest="input_file")
    parser_pharma_addr.add_argument("-o", "--output")
    parser_pharma_addr.set_defaults(func=run_pharma_addr)
    # clinic-label
    parser_clinic_label = sub_parsers.add_parser("clinic-label")
    parser_clinic_label.add_argument("-n", "--count", type=int, help="number of labels")
    parser_clinic_label.add_argument("-o", "--output")
    parser_clinic_label.set_defaults(func=run_clinic_label)
    #
    args = parser.parse_args()
    f = args.func
    kwargs = vars(args)
    del kwargs["func"]
    f(**kwargs)


if __name__ == "__main__":
    run()


