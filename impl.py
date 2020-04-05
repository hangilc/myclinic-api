from typing import Optional, Sequence, Union, List, Dict, Callable, Set

from model import *
import rcpt
import houkatsu
from sqlalchemy import and_, or_, not_, distinct
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
import os
import yaml
from consts import *

CONFIG_DIR = os.environ.get("MYCLINIC_CONFIG")
REFER_LIST = []
CLINIC_INFO = {}
APPLICATION_CONFIG = {}
PRACTICE_CONFIG = {}
DISEASE_EXAMPLES = []
PAPER_SCAN_DIR = None
NAME_MAP_FILE_PATH = None
IYAKUHIN_NAME_MAP = {}
SHINRYOU_NAME_MAP = {}
KIZAI_NAME_MAP = {}
DISEASE_NAME_MAP = {}
DISEASE_ADJ_NAME_MAP = {}
MASTER_MAP_FILE_PATH = None
IYAKUHIN_MASTER_MAP = []
SHINRYOU_MASTER_MAP = []
KIZAI_MASTER_MAP = []
SHINRYOU_BYOUMEI_MAP_FILE = None
POWDER_DRUG_FILE_PATH = None
HOUKATSU_KENSA_FILE_PATH = None


def _hyphen_to_camel(s):
    parts = s.split("-")
    return parts[0] + "".join([x.title() for x in parts[1:]])


def _get_abspath(path):
    return os.path.abspath(path) if path else None


def _load_config_refer_list(config_file):
    with open(config_file, "r", encoding="utf-8") as f:
        global REFER_LIST
        REFER_LIST = yaml.safe_load(f)


def _load_config_clinic_info(config_file):
    with open(config_file, "r", encoding="utf-8") as f:
        global CLINIC_INFO
        for k, v in yaml.safe_load(f).items():
            k = _hyphen_to_camel(k)
            CLINIC_INFO[k] = v


def _load_config_application(config_file):
    with open(config_file, "r", encoding="utf-8") as f:
        global APPLICATION_CONFIG
        global PRACTICE_CONFIG
        global DISEASE_EXAMPLES
        global PAPER_SCAN_DIR
        global NAME_MAP_FILE_PATH
        global SHINRYOU_BYOUMEI_MAP_FILE
        global POWDER_DRUG_FILE_PATH
        APPLICATION_CONFIG = yaml.safe_load(f)
        myclinic = APPLICATION_CONFIG.get("myclinic")
        if myclinic:
            practice = myclinic.get("practice", {})
            for k, v in practice.items():
                k = _hyphen_to_camel(k)
                PRACTICE_CONFIG[k] = v
            dex = myclinic.get("disease-example", [])
            for entry in dex:
                pre = entry.get("pre", [])
                post = entry.get("post", [])
                label = entry.get("label")
                if not label:
                    byoumei = entry.get("byoumei", "")
                    label = "".join(pre + [byoumei] + post)
                ex = {
                    "label": label,
                    "byoumei": entry.get("byoumei"),
                    "adjList": pre + post
                }
                DISEASE_EXAMPLES.append(ex)
            scan = myclinic.get("scanner", {})
            PAPER_SCAN_DIR = _get_abspath(scan.get("paper-scan-directory"))
            NAME_MAP_FILE_PATH = _get_abspath(myclinic.get("name-map-file"))
            SHINRYOU_BYOUMEI_MAP_FILE = _get_abspath(myclinic.get("shinryou-byoumei-file"))
            POWDER_DRUG_FILE_PATH = _get_abspath(myclinic.get("powder-drug-file"))


def _load_config_master_name(config_file):
    with open(config_file, "r", encoding="utf-8") as f:
        global SHINRYOU_NAME_MAP, KIZAI_NAME_MAP, DISEASE_NAME_MAP, DISEASE_ADJ_NAME_MAP
        for line in f:
            line = line.strip()
            if not line or line.startswith(";"):
                continue
            parts = line.split(",")
            if len(parts) == 3:
                (kind, name, code) = parts
                if kind == "s":
                    SHINRYOU_NAME_MAP[name] = int(code)
                elif kind == "k":
                    KIZAI_NAME_MAP[name] = int(code)
                elif kind == "d":
                    DISEASE_NAME_MAP[name] = int(code)
                elif kind == "a":
                    DISEASE_ADJ_NAME_MAP[name] = int(code)
                else:
                    print("Unknown kind in master-name entry:", line)
            else:
                print("Invalid master name entry:", line)


def _load_config_master_map(config_file):
    global MASTER_MAP_FILE_PATH
    MASTER_MAP_FILE_PATH = _get_abspath(config_file)
    delim = re.compile(r"[ ,]")
    re_date = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    with open(config_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(";"):
                continue
            line += " dummy comment"
            (kind, from_code, at, to_code, _) = delim.split(line, maxsplit=4)
            if not re_date.match(at):
                print("invalid date in master-map:", line)
            if kind == "Y":
                mmap = IYAKUHIN_MASTER_MAP
            elif kind == "S":
                mmap = SHINRYOU_MASTER_MAP
            elif kind == "K":
                mmap = KIZAI_MASTER_MAP
            else:
                print("Unknown master map kind:", line)
            mmap.append({"from_code": int(from_code), "to_code": int(to_code), "at": at})


def _load_config(config_dir):
    def config_file(fname):
        return os.path.join(config_dir, fname)

    _load_config_refer_list(config_file("refer-list.yml"))
    _load_config_clinic_info(config_file("clinic-info.yml"))
    _load_config_application(config_file("application.yml"))
    _load_config_master_name(config_file("master-name.txt"))
    _load_config_master_map(config_file("master-map.txt"))
    global HOUKATSU_KENSA_FILE_PATH
    HOUKATSU_KENSA_FILE_PATH = config_file("houkatsu-kensa.xml")


def _resolve_master_map(mmap, code, at):
    at = _normalize_at(at)
    for m in mmap:
        if m["from_code"] == code and m["at"] <= at:
            code = m["to_code"]
    return code


def _resolve_iyakuhin_master_map(code, at):
    return _resolve_master_map(IYAKUHIN_MASTER_MAP, code, at)


def _resolve_shinryou_master_map(code, at):
    return _resolve_master_map(SHINRYOU_MASTER_MAP, code, at)


def _resolve_kizai_master_map(code, at):
    return _resolve_master_map(KIZAI_MASTER_MAP, code, at)


def _resolve_shinryou_name(name) -> Optional[int]:
    return SHINRYOU_NAME_MAP.get(name, None)


def _resolve_kizai_name(name):
    return KIZAI_NAME_MAP.get(name, None)


def _resolve_master(session, master, code_column: Column, code_trans, code, at):
    at = _normalize_at(at)
    print("BEFORE CODE", code)
    code = _resolve_master_map(code_trans, code, at)
    print("AFTER CODE", code)
    return (session.query(master)
            .filter(code_column == code)
            .filter(_valid_at(master, at))
            .one_or_none())


def _resolve_shinryou_master(session, shinryoucode, at) -> Optional[ShinryouMaster]:
    return _resolve_master(session, ShinryouMaster, ShinryouMaster.shinryoucode, SHINRYOU_MASTER_MAP,
                           shinryoucode, at)


def _resolve_iyakuhin_master(session, iyakuhincode, at) -> Optional[IyakuhinMaster]:
    return _resolve_master(session, IyakuhinMaster, IyakuhinMaster.iyakuhincode, IYAKUHIN_MASTER_MAP,
                           iyakuhincode, at)


def resolve_kizai_master(session, kizaicode, at) -> Optional[KizaiMaster]:
    return _resolve_master(session, KizaiMaster, KizaiMaster.kizaicode, KIZAI_MASTER_MAP,
                           kizaicode, at)


def _resolve_master_by_name(session, master, code_column, name_map, code_trans, name, at):
    at = _normalize_at(at)
    code = name_map.get(name)
    if code:
        return _resolve_master(session, master, code_column, code_trans, code, at)
    else:
        return (session.query(master)
                .filter(master.name == name)
                .filter(_valid_at(master, at))
                .one())


def _resolve_shinryou_master_by_name(session, name, at) -> Optional[ShinryouMaster]:
    return _resolve_master_by_name(session, ShinryouMaster, ShinryouMaster.shinryoucode,
                                   SHINRYOU_NAME_MAP, SHINRYOU_MASTER_MAP, name, at)


def _resolve_iyakuhin_master_by_name(session, name, at) -> Optional[IyakuhinMaster]:
    return _resolve_master_by_name(session, IyakuhinMaster, IyakuhinMaster.iyakuhincode,
                                   IYAKUHIN_NAME_MAP, IYAKUHIN_MASTER_MAP, name, at)


def _resolve_kizai_master_by_name(session, name, at) -> Optional[KizaiMaster]:
    return _resolve_master_by_name(session, KizaiMaster, KizaiMaster.kizaicode,
                                   KIZAI_NAME_MAP, KIZAI_MASTER_MAP, name, at)


if os.path.isdir(CONFIG_DIR):
    _load_config(CONFIG_DIR)

ZERO_DATE = "0000-00-00"


def search_byoumei(session, text, at) -> Sequence[ByoumeiMaster]:
    if not text:
        return []
    at = _normalize_at(at)
    return (session.query(ByoumeiMaster)
            .filter(ByoumeiMaster.name.like(f"%{text}%"))
            .filter(_valid_at(ByoumeiMaster, at))
            .all())


def _having_hoken():
    return not_(and_(Visit.shahokokuho_id == 0,
                     Visit.koukikourei_id == 0,
                     Visit.roujin_id == 0,
                     Visit.kouhi_1_id == 0,
                     Visit.kouhi_2_id == 0,
                     Visit.kouhi_3_id == 0))


def list_visit_by_patient_having_hoken(session, patient_id: int, year: int, month: int) -> Sequence[VisitFull2]:
    visits = (session.query(Visit)
              .filter(Visit.patient_id == patient_id)
              .filter(func.year(Visit.visited_at) == year, func.month(Visit.visited_at) == month)
              .filter(_having_hoken())
              .all())
    visit_fulls = [_get_visit_full_2(session, v) for v in visits]
    return [vf for vf in visit_fulls if len(vf.shinryou_list) > 0 or len(vf.drugs) > 0 or len(vf.conducts) > 0]


def list_recently_registered_patients(session, n: Optional[int]) -> Sequence[Patient]:
    if n is None:
        n = 20
    return session.query(Patient).order_by(Patient.patient_id.desc()).limit(n).all()


def list_todays_hotline_in_range(session, after: int, before: int) -> Sequence[Hotline]:
    at = _today_as_sqldate()
    return (session.query(Hotline)
            .filter(func.date(Hotline.posted_at) == at)
            .filter(Hotline.hotline_id > after, Hotline.hotline_id < before)
            .order_by(Hotline.hotline_id)
            .all())


def _today_as_sqldate() -> str:
    return _date_to_sqldate(datetime.date.today())


def _now_as_sqldatetime() -> str:
    return _datetime_to_sqldatetime(datetime.datetime.now())


def _date_to_sqldate(d: datetime.date) -> str:
    return d.strftime("%Y-%m-%d")


def _datetime_to_sqldatetime(d: datetime.datetime) -> str:
    return d.strftime("%Y-%m-%d %H:%M:%S")


def _sqldate_to_date(sqldate) -> datetime.date:
    if isinstance(sqldate, str):
        return datetime.datetime.strptime(sqldate, "%Y-%m-%d").date()
    elif isinstance(sqldate, datetime.datetime):
        return sqldate.date()
    elif isinstance(sqldate, datetime.date):
        return sqldate
    else:
        raise Exception(f"Cannot convert to date {repr(sqldate)}")


def _sqldatetime_to_datetime(sqldatetime) -> datetime.datetime:
    if isinstance(sqldatetime, str):
        return datetime.datetime.strptime(sqldatetime, "%Y-%m-%d %H:%M:%S")
    elif isinstance(sqldatetime, datetime.datetime):
        return sqldatetime
    else:
        raise Exception(f"Cannot convert to date {repr(sqldatetime)}")


def list_todays_visits(session) -> Sequence[VisitPatient]:
    today = _today_as_sqldate()
    rows = (session.query(Visit, Patient).filter(func.date(Visit.visited_at) == today)
            .filter(Visit.patient_id == Patient.patient_id)
            .order_by(Visit.visit_id)
            .all())
    return [VisitPatient(visit=v, patient=p) for (v, p) in rows]


def batch_get_drug_attr(session, drug_ids: Sequence[int]) -> Sequence[DrugAttr]:
    if not drug_ids:
        return []
    return (session.query(DrugAttr)
            .filter(DrugAttr.drug_id.in_(drug_ids))
            .all())


def get_drug_full(session, drug_id):
    (d, m) = (session.query(Drug, IyakuhinMaster)
              .join(Visit, Visit.visit_id == Drug.visit_id)
              .filter(Drug.drug_id == drug_id)
              .filter(Drug.iyakuhincode == IyakuhinMaster.iyakuhincode)
              .filter(IyakuhinMaster.valid_from <= func.date(Visit.visited_at))
              .filter(or_(IyakuhinMaster.valid_upto == "0000-00-00",
                          func.date(Visit.visited_at) <= IyakuhinMaster.valid_upto))
              .one())
    return DrugFull(drug=d, master=m)


def get_shinryou_full(session, shinryou_id):
    return (session.query(Shinryou, ShinryouMaster)
            .join(Visit, Visit.visit_id == Shinryou.visit_id)
            .filter(Shinryou.shinryou_id == shinryou_id)
            .filter(ShinryouMaster.shinryoucode == Shinryou.shinryoucode)
            .filter(ShinryouMaster.valid_from <= func.date(Visit.visited_at))
            .filter(or_(ShinryouMaster.valid_upto == ZERO_DATE,
                        func.date(Visit.visited_at) <= ShinryouMaster.valid_upto))
            .one())


def convert_to_hoken(session, visit: Visit) -> Hoken:
    hoken = Hoken()
    if visit.shahokokuho_id > 0:
        hoken.shahokokuho = get_shahokokuho(session, visit.shahokokuho_id)
    if visit.koukikourei_id > 0:
        hoken.koukikourei = get_koukikourei(session, visit.koukikourei_id)
    if visit.roujin_id > 0:
        hoken.roujin = get_roujin(session, visit.roujin_id)
    if visit.kouhi_1_id > 0:
        hoken.kouhi_1 = get_kouhi(session, visit.kouhi_1_id)
    if visit.kouhi_2_id > 0:
        hoken.kouhi_2 = get_kouhi(session, visit.kouhi_2_id)
    if visit.kouhi_3_id > 0:
        hoken.kouhi_3 = get_kouhi(session, visit.kouhi_3_id)
    return hoken


def batch_delete_drugs(session, drug_ids):
    for drug_id in drug_ids:
        delete_drug(session, drug_id)
    return True


def _list_conduct_kizai_full(session, conduct_id):
    rows = (session.query(ConductKizai, KizaiMaster)
            .join(Conduct, Conduct.conduct_id == ConductKizai.conduct_id)
            .join(Visit, Visit.visit_id == Conduct.visit_id)
            .filter(ConductKizai.conduct_id == conduct_id)
            .filter(KizaiMaster.kizaicode == ConductKizai.kizaicode)
            .filter(KizaiMaster.valid_from <= func.date(Visit.visited_at))
            .filter(or_(KizaiMaster.valid_upto == ZERO_DATE,
                        func.date(Visit.visited_at) <= KizaiMaster.valid_upto))
            .order_by(ConductKizai.conduct_kizai_id)
            .all())
    return [ConductKizaiFull(conduct_kizai=k, master=m) for (k, m) in rows]


def get_conduct_kizai_full(session, conduct_kizai_id) -> ConductKizaiFull:
    (k, m) = (session.query(ConductKizai, KizaiMaster)
              .join(Conduct, Conduct.conduct_id == ConductKizai.conduct_id)
              .join(Visit, Visit.visit_id == Conduct.visit_id)
              .filter(ConductKizai.conduct_kizai_id == conduct_kizai_id)
              .filter(KizaiMaster.kizaicode == ConductKizai.kizaicode)
              .filter(_valid_at(KizaiMaster, func.date(Visit.visited_at)))
              .one())
    return ConductKizaiFull(conduct_kizai=k, master=m)


def find_byoumei_master_by_name(session, name, at) -> Optional[ByoumeiMaster]:
    if not name:
        return None
    at = _normalize_at(at)
    return (session.query(ByoumeiMaster)
            .filter(ByoumeiMaster.name == name)
            .filter(_valid_at(ByoumeiMaster, at))
            .one_or_none())


def list_disease_example():
    return DISEASE_EXAMPLES


def list_drug_full_by_drug_ids(session, drug_ids: Sequence[int]) -> Sequence[DrugFull]:
    print(drug_ids)
    return [get_drug_full(session, drug_id) for drug_id in drug_ids]


def list_wqueue_full(session) -> List[WqueueFull]:
    rows = (session.query(Wqueue, Visit, Patient)
            .filter(Wqueue.visit_id == Visit.visit_id)
            .filter(Patient.patient_id == Visit.patient_id)
            .order_by(Wqueue.visit_id)
            .all())
    return [WqueueFull(wqueue=w, visit=v, patient=p) for (w, v, p) in rows]


def get_shahokokuho(session, shahokokuho_id) -> Shahokokuho:
    return session.query(Shahokokuho).get(shahokokuho_id)


def _batch_resolve_names(session, resolver: Callable[[Session, str, str], Optional[int]], at, args: List[List[str]]) \
        -> Dict[str, int]:
    at = _normalize_at(at)
    result: Dict[str, int] = {}
    for arg in args:
        if len(arg) == 0:
            continue
        key = arg[0]
        if len(arg) > 1:
            arg = arg[1:]
        for name in arg:
            code = resolver(session, name, at)
            if code:
                result[key] = code
    return result


def batch_resolve_shinryou_names(session, at, args: List[List[str]]) -> Dict[str, int]:
    def resolver(arg_session, arg_name, arg_at):
        master = find_shinryou_master_by_name(arg_session, arg_name, arg_at)
        return master.shinryoucode if master else None

    return _batch_resolve_names(session, resolver, at, args)


def delete_conduct_kizai(session, conduct_kizai_id):
    c = session.query(ConductKizai).get(conduct_kizai_id)
    if c:
        session.delete(c)


def get_pharma_queue_full(session, visit_id):
    pq = session.query(PharmaQueue).get(visit_id)
    visit = get_visit(session, visit_id)
    patient = get_patient(session, visit.patient_id)
    wq = session.query(Wqueue).get(visit_id)
    return PharmaQueueFull(pharma_queue=pq, patient=patient, wqueue=wq, visit_id=visit_id)


def enter_shinryou_attr(session, attr) -> bool:
    session.merge(attr)
    return True


def delete_gazou_label(session, conduct_id) -> bool:
    g = session.query(GazouLabel).get(conduct_id)
    if g:
        session.delete(g)
    return True


def find_shinryou_attr(session, shinryou_id) -> ShinryouAttr:
    return session.Query(ShinryouAttr).get(shinryou_id)


def _count_pages(total, items_per_page):
    return (total + items_per_page - 1) // items_per_page


def _get_hoken_for_visit(session, visit):
    shahokokuho = None if visit.shahokokuho_id == 0 else session.query(Shahokokuho).get(visit.shahokokuho_id)
    koukikourei = None if visit.koukikourei_id == 0 else session.query(Koukikourei).get(visit.koukikourei_id)
    roujin = None if visit.roujin_id == 0 else session.query(Roujin).get(visit.roujin_id)
    kouhi_1 = None if visit.kouhi_1_id == 0 else session.query(Kouhi).get(visit.kouhi_1_id)
    kouhi_2 = None if visit.kouhi_2_id == 0 else session.query(Kouhi).get(visit.kouhi_2_id)
    kouhi_3 = None if visit.kouhi_3_id == 0 else session.query(Kouhi).get(visit.kouhi_3_id)
    return Hoken(shahokokuho=shahokokuho,
                 koukikourei=koukikourei,
                 roujin=roujin,
                 kouhi_1=kouhi_1,
                 kouhi_2=kouhi_2,
                 kouhi_3=kouhi_3)


def _get_visit_full_2(session, visit):
    visit_id = visit.visit_id
    texts = list_text(session, visit.visit_id)
    drug_fulls = list_drug_full(session, visit_id)
    shinryou_full_list = list_shinryou_full(session, visit_id)
    conducts = session.query(Conduct).filter_by(visit_id=visit_id).order_by(Conduct.conduct_id).all()
    conduct_fulls = [get_conduct_full(session, c.conduct_id) for c in conducts]
    hoken = _get_hoken_for_visit(session, visit)
    charge = session.query(Charge).get(visit_id)
    return VisitFull2(visit=visit, texts=texts, drugs=drug_fulls, shinryou_list=shinryou_full_list,
                      conducts=conduct_fulls, hoken=hoken, charge=charge)


def list_visit_full_2(session, patient_id, page):
    items_per_page = 10
    total = session.query(Visit).filter_by(patient_id=patient_id).count()
    total_pages = _count_pages(total, items_per_page)
    start = page * items_per_page
    end = (page + 1) * items_per_page
    visits = session.query(Visit).filter_by(patient_id=patient_id).order_by(Visit.visit_id.desc())[start:end]
    return {
        "page": page,
        "totalPages": total_pages,
        "visits": [_get_visit_full_2(session, v) for v in visits]
    }


def get_text(session, text_id):
    return session.query(Text).get(text_id)


def enter_conduct_full(session, arg: ConductEnterRequest) -> ConductFull:
    conduct = Conduct(conduct_id=None, visit_id=arg.visit_id, kind=arg.kind)
    session.add(conduct)
    session.flush()
    conduct_id = conduct.conduct_id
    if arg.gazou_label:
        g = GazouLabel(conduct_id=conduct_id, label=arg.gazou_label)
        session.add(g)
    if arg.shinryou_list:
        for cs in arg.shinryou_list:
            cs.conduct_shinryou_id = None
            cs.conduct_id = conduct_id
            session.add(cs)
    if arg.drugs:
        for cd in arg.drugs:
            cd.conduct_drug_id = None
            cd.conduct_id = conduct_id
            session.add(cd)
    if arg.kizai_list:
        for ck in arg.kizai_list:
            ck.conduct_kizai_id = None
            ck.conduct_id = conduct_id
            session.add(ck)
    session.flush()
    return get_conduct_full(session, conduct_id)


def find_shouki(session, visit_id) -> Shouki:
    return session.query(Shouki).find_by(visit_id=visit_id).one_or_none()


def list_conduct_full_by_ids(session, conduct_ids) -> List[ConductFull]:
    return [get_conduct_full(session, conduct_id) for conduct_id in conduct_ids]


def get_kouhi(session, kouhi_id) -> Kouhi:
    return session.query(Kouhi).get(kouhi_id)


def enter_shouki(session, shouki: Shouki) -> bool:
    session.add(shouki)
    return True


def list_hokensho(patient_id: int) -> List[str]:
    if PAPER_SCAN_DIR:
        result = []
        pat = re.compile(rf"{patient_id}-hokensho-.+\.(jpg|jpeg|bmp)$")
        # noinspection PyTypeChecker
        files = os.listdir(os.path.join(PAPER_SCAN_DIR, str(patient_id)))
        for f in files:
            if pat.search(f):
                result.append(os.path.basename(f))
        return result
    else:
        raise Exception("Cannot find paper scan directory.")


def delete_koukikourei(session, koukikourei: Koukikourei) -> bool:
    session.delete(koukikourei)
    return True


def list_disease_full(session, patient_id: int) -> List[DiseaseFull]:
    rows = (session.query(Disease, ByoumeiMaster)
            .filter(Disease.patient_id == patient_id)
            .filter(ByoumeiMaster.shoubyoumeicode == Disease.shoubyoumeicode)
            .filter(_valid_at(ByoumeiMaster, Disease.start_date))
            .order_by(Disease.disease_id)
            .all())
    return [DiseaseFull(disease=d, master=m, adj_list=_list_disease_adj_full(session, d.disease_id))
            for (d, m) in rows]


def list_hoken(session, patient_id: int) -> HokenList:
    return HokenList(
        shahokokuho_list=_list_shahokokuho_by_patient(session, patient_id),
        koukikourei_list=_list_koukikourei_by_patient(session, patient_id),
        roujin_list=_list_roujin_by_patient(session, patient_id),
        kouhi_list=_list_kouhi_by_patient(session, patient_id)
    )


def _list_shahokokuho_by_patient(session, patient_id, order=Shahokokuho.shahokokuho_id.desc()) -> List[Shahokokuho]:
    return (session.query(Shahokokuho)
            .filter(Shahokokuho.patient_id == patient_id)
            .order_by(order)
            .all())


def _list_koukikourei_by_patient(session, patient_id, order=Koukikourei.koukikourei_id.desc()) -> List[Koukikourei]:
    return (session.query(Koukikourei)
            .filter(Koukikourei.patient_id == patient_id)
            .order_by(order)
            .all())


def _list_roujin_by_patient(session, patient_id, order=Roujin.roujin_id.desc()) -> List[Roujin]:
    return (session.query(Roujin)
            .filter(Roujin.patient_id == patient_id)
            .order_by(order)
            .all())


def _list_kouhi_by_patient(session, patient_id, order=Kouhi.kouhi_id.desc()) -> List[Kouhi]:
    return (session.query(Kouhi)
            .filter(Kouhi.patient_id == patient_id)
            .order_by(order)
            .all())


def delete_shouki(session, visit_id):
    s = session.query(Shouki).get(visit_id)
    if s:
        session.delete(s)


def find_drug_attr(session, drug_id):
    return session.query(DrugAttr).filter_by(drug_id=drug_id).one_or_none()


def update_hoken(session, hoken):
    visit = session.query(Visit).get(hoken.visit_id)
    if hoken.shahokokuho_id is not None:
        visit.shahokokuho_id = hoken.shahokokuho_id
    if hoken.koukikourei_id is not None:
        visit.koukikourei_id = hoken.koukikourei_id
    if hoken.roujin_id is not None:
        visit.roujin_id = hoken.roujin_id
    if hoken.kouhi_1_id is not None:
        visit.kouhi_1_id = hoken.kouhi_1_id
    if hoken.kouhi_2_id is not None:
        visit.kouhi_2_id = hoken.kouhi_2_id
    if hoken.kouhi_3_id is not None:
        visit.kouhi_3_id = hoken.kouhi_3_id
    return True


def list_visit_text_drug_by_patient_and_iyakuhincode(session, patient_id, iyakuhincode, page) -> VisitTextDrugPage:
    result = VisitTextDrugPage()
    q = (session.query(Visit)
         .join(Drug, Drug.visit_id == Visit.visit_id)
         .filter(Visit.patient_id == patient_id)
         .filter(Drug.iyakuhincode == iyakuhincode))
    total = q.count()
    items_per_page = 10
    total_pages = _count_pages(total, items_per_page)
    visits = q.order_by(Visit.visit_id).offset(page * items_per_page).limit(items_per_page).all()
    result.total_pages = total_pages
    result.page = page
    result.visit_text_drugs = []
    result.visit_text_drugs = [VisitTextDrug(
        visit=v,
        texts=list_text(session, v.visit_id),
        drugs=list_drug_full(session, v.visit_id)
    ) for v in visits]
    return result


def get_wqueue_full(session, visit_id) -> WqueueFull:
    (wq, v, p) = (session.query(Wqueue, Visit, Patient)
                  .filter(Wqueue.visit_id == visit_id)
                  .filter(Visit.visit_id == visit_id)
                  .filter(Patient.patient_id == Visit.patient_id)
                  .one())
    return WqueueFull(wqueue=wq, visit=v, patient=p)


def list_shinryou_full(session, visit_id):
    rows = (session.query(Shinryou, ShinryouMaster)
            .join(Visit, Visit.visit_id == Shinryou.visit_id)
            .filter(Shinryou.visit_id == visit_id)
            .filter(ShinryouMaster.shinryoucode == Shinryou.shinryoucode)
            .filter(ShinryouMaster.valid_from <= func.date(Visit.visited_at))
            .filter(or_(ShinryouMaster.valid_upto == ZERO_DATE,
                        func.date(Visit.visited_at) <= ShinryouMaster.valid_upto))
            .order_by(Shinryou.shinryoucode)
            .all())
    return [ShinryouFull(shinryou=s, master=m) for (s, m) in rows]


def search_shinryou_master(session, text, at):
    if not text:
        return []
    else:
        at = _normalize_at(at)
        return (session.query(ShinryouMaster)
                .filter(ShinryouMaster.name.like(f"%{text}%"))
                .filter(ShinryouMaster.valid_from <= at)
                .filter(or_(ShinryouMaster.valid_upto == "0000-00-00",
                            at <= ShinryouMaster.valid_upto))
                .order_by(ShinryouMaster.shinryoucode)
                .all())


def _enter_kotsuen_teiryou(session, visit_id) -> int:
    conduct = Conduct(conduct_id=None, visit_id=visit_id, kind=ConductKindGazou)
    session.add(conduct)
    session.flush()
    conduct_id = conduct.conduct_id
    _enter_gazou_label(session, conduct_id, "骨塩定量に使用")
    _enter_conduct_shinryou_by_name(session, conduct_id, "骨塩定量ＭＤ法")
    _enter_conduct_kiazi_by_name(session, conduct_id, "四ツ切", 1)
    return conduct_id


def _enter_shinryou_by_name(session, visit_id, name) -> int:
    visit = session.query(Visit).get(visit_id)
    at = _normalize_at(visit.visited_at)
    master = resolve_shinryou_master_by_name(session, name, at)
    if not master:
        raise Exception(f"{name}を追加できません。")
    shinryou = Shinryou(shinryou_id=None, visit_id=visit_id, shinryoucode=master.shinryoucode)
    return enter_shinryou(session, shinryou)


def batch_enter_shinryou_by_name(session, names, visit_id) -> BatchEnterResult:
    result = BatchEnterResult(shinryou_ids=[], conduct_ids=[])
    for name in names:
        if name == "骨塩定量":
            result.conduct_ids.append(_enter_kotsuen_teiryou(session, visit_id))
            continue
        shinryou_id = _enter_shinryou_by_name(session, visit_id, name)
        if shinryou_id:
            result.shinryou_ids.append(shinryou_id)
    return result


def _enter_gazou_label(session, conduct_id, label: str) -> None:
    gazou = GazouLabel(conduct_id=conduct_id, label=label)
    session.add(gazou)


def _enter_conduct_kiazi_by_name(session, conduct_id, name, amount) -> int:
    conduct = session.query(Conduct).get(conduct_id)
    visit = session.query(Visit).get(conduct.visit_id)
    at = _normalize_at(visit.visited_at)
    master = resolve_kizai_master_by_name(session, name, at)
    if not master:
        raise Exception(f"{name}を追加できません。")
    kizai = ConductKizai(conduct_id=conduct_id, kizaicode=master.kizaicode, amount=amount)
    session.add(kizai)
    return kizai.conduct_kizai_id


def enter_conduct_kizai(session, conduct_kizai: ConductKizai) -> int:
    conduct_kizai.conduct_kizai_id = None
    session.add(conduct_kizai)
    session.flush()
    # noinspection PyTypeChecker
    return conduct_kizai.conduct_kizai_id


def batch_enter_drugs(session, drugs: List[Drug]) -> List[int]:
    return [enter_drug(session, drug) for drug in drugs]


def delete_disease(session, disease_id) -> bool:
    d = session.query(Disease).get(disease_id)
    if d:
        session.delete(d)
    return True


def batch_resolve_iyakuhin_master(session, iyakuhincodes: List[int], at) -> Dict[int, str]:
    at = _normalize_at(at)
    return {code: resolve_iyakuhin_master(session, code, at) for code in iyakuhincodes}


def get_clinic_info():
    return CLINIC_INFO


def list_all_pharma_drug_names(session) -> List[PharmaDrugName]:
    rows = (session.query(IyakuhinMaster.iyakuhincode, IyakuhinMaster.name, IyakuhinMaster.yomi)
            .join(PharmaDrug, PharmaDrug.iyakuhincode == IyakuhinMaster.iyakuhincode)
            .group_by(IyakuhinMaster.iyakuhincode, IyakuhinMaster.name, IyakuhinMaster.yomi)
            .order_by(IyakuhinMaster.yomi)
            .all())
    return [PharmaDrugName(iyakuhincode=code, name=name, yomi=yomi) for (code, name, yomi) in rows]


def list_payment(session, visit_id) -> List[Payment]:
    return (session.query(Payment)
            .filter(Payment.visit_id == visit_id)
            .order_by(Payment.visit_id.desc())
            .all())


def list_visit_id_visited_at_by_patient_and_iyakuhincode(session, patient_id: int, iyakuhincode: int) \
        -> List[VisitIdVisitedAt]:
    rows = (session.query(Visit.visit_id, Visit.visited_at)
            .join(Drug, Drug.visit_id == Visit.visit_id)
            .filter(Visit.patient_id == patient_id)
            .filter(Drug.iyakuhincode == iyakuhincode)
            .order_by(Visit.visit_id)
            .all())
    return [VisitIdVisitedAt(visit_id=visit_id, visited_at=visited_at) for (visit_id, visited_at) in rows]


def batch_delete_shinryou(session, shinryou_ids: List[int]) -> bool:
    for shinryou_id in shinryou_ids:
        delete_shinryou(session, shinryou_id)
    return True


def _list_disease_adj_full(session, disease_id):
    rows = (session.query(DiseaseAdj, ShuushokugoMaster)
            .filter(DiseaseAdj.disease_id == disease_id)
            .filter(DiseaseAdj.shuushokugocode == ShuushokugoMaster.shuushokugocode)
            .order_by(DiseaseAdj.disease_adj_id)
            .all())
    return [DiseaseAdjFull(d, m) for (d, m) in rows]


def list_current_disease_full(session, patient_id):
    diseases = (session.query(Disease, ByoumeiMaster)
                .filter(Disease.patient_id == patient_id)
                .filter(Disease.end_reason == "N")
                .filter(Disease.shoubyoumeicode == ByoumeiMaster.shoubyoumeicode)
                .filter(ByoumeiMaster.valid_from <= Disease.start_date)
                .filter(or_(ByoumeiMaster.valid_upto == "0000-00-00",
                            Disease.start_date <= ByoumeiMaster.valid_upto))
                .order_by(Disease.disease_id)
                .all())
    return [DiseaseFull(d, m, _list_disease_adj_full(session, d.disease_id)) for (d, m) in diseases]


def enter_disease(session, disease_new: DiseaseNew) -> int:
    d = disease_new.disease
    a: List[DiseaseAdj] = disease_new.adj_list
    d.disease_id = None
    session.add(d)
    session.flush()
    disease_id = d.disease_id
    for adj in a:
        adj.disease_adj_id = None
        adj.disease_id = disease_id
        session.add(adj)
    # noinspection PyTypeChecker
    return disease_id


def get_charge(session, visit_id) -> Charge:
    return session.query(Charge).get(visit_id)


def batch_copy_shinryou(session, visit_id, src_list: List[Shinryou]) -> List[int]:
    visit = get_visit(session, visit_id)
    at = _normalize_at(visit.visited_at)
    shinryou_ids = []
    for src in src_list:
        master = resolve_shinryou_master(session, src.shinryoucode, at)
        if not master:
            raise Exception(f"診療行為を入力できません。（{src.shinryoucode}）")
        dst = Shinryou(visit_id=visit_id, shinryoucode=master.shinryoucode)
        shinryou_ids.append(enter_shinryou(session, dst))
    return shinryou_ids


def _enter_conduct_shinryou_by_name(session, conduct_id, name) -> int:
    conduct = session.query(Conduct).get(conduct_id)
    visit = session.query(Visit).get(conduct.visit_id)
    at = _normalize_at(visit.visited_at)
    master = resolve_shinryou_master_by_name(session, name, at)
    if not master:
        raise Exception(f"{name}を追加できません。")
    cs = ConductShinryou(conduct_shinryou_id=None, conduct_id=conduct_id, shinryoucode=master.shinryoucode)
    session.add(cs)
    return cs.conduct_shinryou_id


def enter_conduct_shinryou(session, conduct_shinryou: ConductShinryou) -> int:
    conduct_shinryou.conduct_shinryou_id = None
    session.add(conduct_shinryou)
    session.flush()
    # noinspection PyTypeChecker
    return conduct_shinryou.conduct_shinryou_id


def enter_kouhi(session, kouhi: Kouhi) -> int:
    kouhi.kouhi_id = None
    session.add(kouhi)
    session.flush()
    # noinspection PyTypeChecker
    return kouhi.kouhi_id


def list_all_presc_example(session) -> List[PrescExampleFull]:
    rows = (session.query(PrescExample, IyakuhinMaster)
            .filter(IyakuhinMaster.iyakuhincode == PrescExample.iyakuhincode)
            .filter(IyakuhinMaster.valid_from == PrescExample.master_valid_from)
            .all())
    return [PrescExampleFull(presc_example=e, master=m) for (e, m) in rows]


def finish_cashier(session, payment: Payment) -> bool:
    session.add(payment)
    visit_id = payment.visit_id
    pq = session.query(PharmaQueue).get(visit_id)
    wq: Wqueue = session.query(Wqueue).get(visit_id)
    if wq:
        if pq:
            wq.wait_state = WqueueStateWaitDrug
        else:
            session.delete(wq)
    return True


def enter_drug_attr(session, attr: DrugAttr) -> bool:
    session.add(attr)
    return True


def enter_drug(session, drug) -> int:
    drug.drug_id = None
    session.add(drug)
    session.flush()
    # noinspection PyTypeChecker
    return drug.drug_id


def delete_pharma_drug(session, iyakuhincode: int) -> bool:
    p = session.query(PharmaDrug).get(iyakuhincode)
    if p:
        session.delete(p)
    return True


def update_patient(session, patient: Patient) -> bool:
    session.merge(patient)
    return True


def delete_text(session, text_id: int) -> bool:
    text = session.query(Text).get(text_id)
    if text:
        session.delete(text)
    return True


def modify_charge(session, visit_id: int, charge_amount: int) -> bool:
    charge = session.query(Charge).get(visit_id)
    if charge:
        charge.charge = charge_amount
    else:
        charge = Charge(visit_id=visit_id, charge=charge_amount)
        session.add(charge)
    return True


def list_available_hoken(session: Session, patient_id: int, at) -> Hoken:
    at = _normalize_at(at)
    shahokokuho = (session.query(Shahokokuho).filter_by(patient_id=patient_id)
                   .filter(Shahokokuho.valid_from <= at)
                   .filter(or_(Shahokokuho.valid_upto == "0000-00-00",
                               at <= Shahokokuho.valid_upto))
                   .order_by(Shahokokuho.shahokokuho_id.desc())
                   .first())
    koukikourei = (session.query(Koukikourei).filter_by(patient_id=patient_id)
                   .filter(Shahokokuho.valid_from <= at)
                   .filter(or_(Shahokokuho.valid_upto == "0000-00-00",
                               at <= Shahokokuho.valid_upto))
                   .order_by(Koukikourei.koukikourei_id.desc())
                   .first())
    roujin = (session.query(Roujin).filter_by(patient_id=patient_id)
              .filter(Shahokokuho.valid_from <= at)
              .filter(or_(Shahokokuho.valid_upto == "0000-00-00",
                          at <= Shahokokuho.valid_upto))
              .order_by(Roujin.roujin_id.desc())
              .first())
    kouhi = (session.query(Roujin).filter_by(patient_id=patient_id)
             .filter(Shahokokuho.valid_from <= at)
             .filter(or_(Shahokokuho.valid_upto == "0000-00-00",
                         at <= Shahokokuho.valid_upto))
             .all())
    kouhi_1 = None if len(kouhi) < 1 else kouhi[0]
    kouhi_2 = None if len(kouhi) < 2 else kouhi[1]
    kouhi_3 = None if len(kouhi) < 3 else kouhi[2]
    return Hoken(
        shahokokuho=shahokokuho,
        koukikourei=koukikourei,
        roujin=roujin,
        kouhi_1=kouhi_1,
        kouhi_2=kouhi_2,
        kouhi_3=kouhi_3
    )


def update_drug(session, drug):
    session.merge(drug)
    return True


def find_gazou_label(session, conduct_id) -> Optional[GazouLabel]:
    return session.query(GazouLabel).get(conduct_id)


def delete_conduct_shinryou(session, conduct_shinryou_id: int) -> bool:
    s = session.query(ConductShinryou).get(conduct_shinryou_id)
    if s:
        session.delete(s)
    return True


def list_pharma_queue_for_today(session) -> List[PharmaQueueFull]:
    today = _today_as_sqldate()
    visit_patients = (session.query(Visit, Patient)
                      .filter(func.date(Visit.visited_at) == today)
                      .filter(Patient.patient_id == Visit.patient_id)
                      .order_by(Visit.visit_id)
                      .all())
    wq_map = {wq.visit_id: wq for wq in session.query(Wqueue).all()}
    pq_map = {pq.visit_id: pq for pq in session.query(PharmaQueue).all()}
    return [PharmaQueueFull(
        visit_id=v.visit_id,
        patient=p,
        pharma_queue=pq_map.get(v.visit_id),
        wqueue=wq_map.get(v.visit_id)
    ) for (v, p) in visit_patients]


def delete_kouhi(session, kouhi: Kouhi) -> bool:
    session.delete(kouhi)
    return True


def enter_hotline(session, hotline: Hotline) -> int:
    hotline.hotline_id = None
    session.add(hotline)
    session.flush()
    # noinspection PyTypeChecker
    return hotline.hotline_id


def list_recent_visits(session, page, items_per_page):
    if page is None:
        page = 0
    if items_per_page is None:
        items_per_page = 30
    start = page * items_per_page
    end = (page + 1) * items_per_page
    rows = (session.query(Visit, Patient).filter(Visit.patient_id == Patient.patient_id)
                .order_by(Visit.visit_id.desc())[start:end])
    return [VisitPatient(visit=v, patient=p) for (v, p) in rows]


def delete_conduct(session, conduct_id) -> bool:
    c = session.query(Conduct).get(conduct_id)
    if c:
        session.delete(c)
    return True


def list_pharma_queue_for_prescription(session) -> List[PharmaQueueFull]:
    wq_map = {wq.visit_id: wq for wq in session.query(Wqueue).all()}
    pq_patients = (session.query(PharmaQueue, Patient)
                   .join(Visit, Visit.visit_id == PharmaQueue.visit_id)
                   .filter(Patient.patient_id == Visit.patient_id)
                   .order_by(PharmaQueue.visit_id)
                   .all())
    return [PharmaQueueFull(
        pharma_queue=pq,
        patient=p,
        visit_id=pq.visit_id,
        wqueue=wq_map.get(pq.visit_id)
    ) for (pq, p) in pq_patients]


def get_drug(session, drug_id):
    return session.query(Drug).get(drug_id)


def enter_koukikourei(session, koukikourei: Koukikourei) -> int:
    koukikourei.koukikourei_id = None
    session.add(koukikourei)
    session.flush()
    # noinspection PyTypeChecker
    return koukikourei.koukikourei_id


def find_shinryou_master_by_name(session, name, at) -> Optional[ShinryouMaster]:
    at = _normalize_at(at)
    return (session.query(ShinryouMaster)
            .filter_by(name=name)
            .filter(ShinryouMaster.valid_from <= at)
            .filter(or_(ShinryouMaster.valid_upto == ZERO_DATE,
                        at <= ShinryouMaster.valid_upto))
            .one_or_none())


def _valid_at(master, at):
    return and_(master.valid_from <= at,
                or_(master.valid_upto == ZERO_DATE,
                    at <= master.valid_upto))


def _find_kizai_master_by_name(session, name, at) -> Optional[KizaiMaster]:
    at = _normalize_at(at)
    return (session.query(KizaiMaster)
            .filter_by(name=name)
            .filter(_valid_at(KizaiMaster, at))
            .one_or_none())


def update_shinryou(session, shinryou: Shinryou) -> bool:
    session.merge(shinryou)
    return True


def get_patient(session, patient_id):
    return session.query(Patient).get(patient_id)


def page_disease_full(session, patient_id, page, items_per_page) -> List[DiseaseFull]:
    q = (session.query(Disease, ByoumeiMaster)
         .filter(Disease.patient_id == patient_id)
         .filter(ByoumeiMaster.shoubyoumeicode == Disease.shoubyoumeicode)
         .filter(_valid_at(ByoumeiMaster, Disease.start_date)))
    # total = q.count()
    # total_pages = _count_pages(total, items_per_page)
    rows = q.order_by(Disease.disease_id.desc()).offset(page * items_per_page).limit(items_per_page).all()
    return [DiseaseFull(
        disease=d,
        master=m,
        adj_list=_list_disease_adj_full(session, d.disease_id)
    ) for (d, m) in rows]


def batch_get_shinryou_attr(session, shinryou_ids):
    return session.query(ShinryouAttr).filter(ShinryouAttr.shinryou_id.in_(shinryou_ids)).all()


def batch_get_shouki(session, visit_ids):
    return session.query(Shouki).filter(Shouki.visit_id.in_(visit_ids)).all()


def get_conduct(session, conduct_id) -> Conduct:
    return session.query(Conduct).get(conduct_id)


def enter_inject(session, visit_id, kind, iyakuhincode, amount) -> int:
    d = ConductDrug(iyakuincode=iyakuhincode, amount=amount)
    req = ConductEnterRequest(visit_id=visit_id, kind=kind, drugs=[d])
    return enter_conduct_full(session, req).conduct.conduct_id


def delete_conduct_drug(session, conduct_drug_id: int) -> bool:
    d = session.query(ConductDrug).get(conduct_drug_id)
    if d:
        session.delete(d)
    return True


def search_presc_example(session, text):
    rows = (session.query(PrescExample, IyakuhinMaster)
            .filter(PrescExample.iyakuhincode == IyakuhinMaster.iyakuhincode)
            .filter(PrescExample.master_valid_from == IyakuhinMaster.valid_from)
            .filter(IyakuhinMaster.name.like(f"%{text}%"))
            .order_by(IyakuhinMaster.yomi)
            .all())
    return [PrescExampleFull(presc_example=p, master=m) for (p, m) in rows]


def search_patient(session, text):
    text = text.strip()
    if text == "":
        return []
    if text.isdigit():
        patient_id = int(text)
        return session.query(Patient).filter_by(patient_id=patient_id).all()
    else:
        parts = text.split(maxsplit=1)
        if len(parts) == 1:
            x = f"%{text}%"
            return (session.query(Patient)
                    .filter(or_(Patient.last_name.like(x), Patient.first_name.like(x),
                                Patient.last_name_yomi.like(x), Patient.first_name_yomi.like(x)))
                    .order_by(Patient.last_name_yomi, Patient.first_name_yomi)
                    .all())
        else:
            a = f"%{parts[0]}%"
            b = f"%{parts[1]}"
            return (session.query(Patient)
                    .filter(and_(or_(Patient.last_name.like(a), Patient.last_name_yomi.like(a)),
                                 or_(Patient.first_name.like(b), Patient.first_name_yomi.like(b))))
                    .order_by(Patient.last_name_yomi, Patient.first_name_yomi)
                    .all())


def update_koukikourei(session, koukikourei) -> bool:
    session.merge(koukikourei)
    return True


def delete_roujin(session, roujin: Roujin) -> bool:
    session.delete(roujin)
    return True


def delete_drug_tekiyou(session, drug_id) -> bool:
    attr = session.query(DrugAttr).get(drug_id)
    if attr:
        attr.tekiyou = None
    return True


def get_master_map_config_file_path() -> StringResult:
    return StringResult(value=MASTER_MAP_FILE_PATH)


def find_pharma_drug(session, iyakuhincode: int) -> Optional[PharmaDrug]:
    return session.query(PharmaDrug).filter(PharmaDrug.iyakuhincode == iyakuhincode).one_or_none()


def resolve_shinryoucode(session, shinryoucode, at) -> int:
    at = _normalize_at(at)
    m = resolve_shinryou_master(session, shinryoucode, at)
    if m:
        return m.shinryoucode
    else:
        raise Exception(f"Cannot find shinryou master ({shinryoucode})")


def _normalize_at(at: Union[str, datetime.datetime, datetime.date]) -> str:
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


def _normalize_datetime(dt: Union[str, datetime.datetime]) -> str:
    if isinstance(dt, str):
        return dt
    elif isinstance(dt, datetime.datetime):
        return _datetime_to_sqldatetime(dt)
    else:
        raise Exception("Cannot handle as datetime: " + repr(dt))


def resolve_iyakuhin_master(session, iyakuhincode, at):
    return _resolve_iyakuhin_master(session, iyakuhincode, at)


def list_drug_full(session, visit_id):
    rows = (session.query(Drug, IyakuhinMaster)
            .join(Visit, Visit.visit_id == Drug.visit_id)
            .filter(Drug.visit_id == visit_id)
            .filter(IyakuhinMaster.iyakuhincode == Drug.iyakuhincode)
            .filter(IyakuhinMaster.valid_from <= func.date(Visit.visited_at))
            .filter(or_(IyakuhinMaster.valid_upto == ZERO_DATE,
                        func.date(Visit.visited_at) <= IyakuhinMaster.valid_upto))
            .order_by(Drug.drug_id)
            .all())
    return [DrugFull(drug=d, master=m) for (d, m) in rows]


def list_wqueue_full_for_exam(session):
    wqueue_for_exam_states = [WqueueStateWaitExam, WqueueStateInExam, WqueueStateWaitReExam]
    wq = (session.query(Wqueue, Visit, Patient).filter(Wqueue.wait_state.in_(wqueue_for_exam_states))
          .filter(Wqueue.visit_id == Visit.visit_id)
          .filter(Visit.patient_id == Patient.patient_id)
          .order_by(Wqueue.visit_id).all())
    return [WqueueFull(wqueue=wq, visit=v, patient=p) for (wq, v, p) in wq]


def update_shouki(session, shouki) -> bool:
    session.merge(shouki)
    return True


def batch_resolve_byoumei_names(session, at, args):
    def resolver(arg_session, arg_name, arg_at):
        master = find_byoumei_master_by_name(arg_session, arg_name, arg_at)
        return master.shoubyoumeicode if master else None

    return _batch_resolve_names(session, resolver, at, args)


def presc_done(session: Session, visit_id: int) -> bool:
    for drug in session.query(Drug).filter_by(visit_id=visit_id).all():
        drug.prescribed = 1
    pq = session.query(PharmaQueue).get(visit_id)
    if pq:
        session.delete(pq)
    wq = session.query(Wqueue).get(visit_id)
    if wq:
        session.delete(wq)
    return True


def search_text_globally(session: Session, text: str, page: int) -> TextVisitPatientPage:
    q = (session.query(Text, Visit, Patient)
         .filter(Text.content.like(f"%{text}%"))
         .filter(Visit.visit_id == Text.visit_id)
         .filter(Patient.patient_id == Visit.patient_id))
    total = q.count()
    items_per_page = 10
    total_pages = _count_pages(total, items_per_page)
    return TextVisitPatientPage(
        page=page,
        total_pages=total_pages,
        text_visit_patients=[TextVisitPatient(
            text=t,
            visit=v,
            patient=p
        ) for (t, v, p) in q.order_by(Text.text_id.desc()).offset(page * items_per_page).limit(items_per_page).all()]
    )


def enter_shinryou(session, shinryou: Shinryou) -> int:
    shinryou.shinryou_id = None
    session.add(shinryou)
    session.flush()
    # noinspection PyTypeChecker
    return shinryou.shinryou_id


def set_drug_tekiyou(session, drug_id, tekiyou: str) -> DrugAttr:
    attr = session.query(DrugAttr).get(drug_id)
    if attr:
        attr.tekiyou = tekiyou
    else:
        attr = DrugAttr(drug_id=drug_id, tekiyou=tekiyou)
        session.add(attr)
        session.flush()
    return attr


def enter_pharma_drug(session, pharma_drug: PharmaDrug) -> bool:
    session.add(pharma_drug)
    return True


def _to_last_day_of_the_month(date: datetime.date) -> datetime.date:
    d = date + datetime.timedelta(days=31)
    d = datetime.date(d.year, d.month, 1)
    d -= datetime.timedelta(days=1)
    return d


def list_disease_by_patient_at(session: Session, patient_id: int, year: int, month: int) -> List[DiseaseFull]:
    valid_from = datetime.date(year, month, 1)
    valid_upto = _to_last_day_of_the_month(valid_from)
    valid_from_str = _date_to_sqldate(valid_from)
    valid_upto_str = _date_to_sqldate(valid_upto)
    disease_ids = (session.query(Disease.disease_id)
                   .filter(Disease.patient_id == patient_id)
                   .filter(or_(Disease.end_reason == DiseaseEndReasonNotEnded,
                               and_(Disease.start_date <= valid_upto_str,
                                    or_(Disease.end_date == ZERO_DATE,
                                        Disease.end_date >= valid_from_str)))))
    return [get_disease_full(session, disease_id) for (disease_id,) in disease_ids]


def get_conduct_full(session, conduct_id):
    conduct = session.query(Conduct).get(conduct_id)
    return ConductFull(conduct=conduct,
                       gazou_label=session.query(GazouLabel).get(conduct_id),
                       conduct_shinryou_list=_list_conduct_shinryou_full(session, conduct_id),
                       conduct_drugs=_list_conduct_drug_full(session, conduct_id),
                       conduct_kizai_list=_list_conduct_kizai_full(session, conduct_id))


def list_iyakuhin_for_patient(session: Session, patient_id: int) -> List[IyakuhincodeName]:
    rows = (session.query(Drug.iyakuhincode, IyakuhinMaster.name)
            .join(Visit, Visit.visit_id == Drug.visit_id)
            .filter(Visit.patient_id == patient_id)
            .filter(IyakuhinMaster.iyakuhincode == Drug.iyakuhincode)
            .filter(_valid_at(IyakuhinMaster, func.date(Visit.visited_at)))
            .group_by(Drug.iyakuhincode, IyakuhinMaster.name)
            .order_by(IyakuhinMaster.yomi))
    return [IyakuhincodeName(
        iyakuhincode=code,
        name=name
    ) for (code, name) in rows]


def search_shuushokugo(session: Session, text: str) -> List[ShuushokugoMaster]:
    return session.query(ShuushokugoMaster).filter(ShuushokugoMaster.name.like(f"%{text}%")).all()


def delete_shahokokuho(session: Session, shahokokuho: Shahokokuho) -> bool:
    session.delete(shahokokuho)
    return True


def list_visit_charge_patient_at(session: Session, at: Union[str, datetime.datetime, datetime.date]) \
        -> List[VisitChargePatient]:
    at = _normalize_at(at)
    rows = (session.query(Visit, Charge, Patient)
            .filter(func.date(Visit.visited_at) == at)
            .filter(Charge.visit_id == Visit.visit_id)
            .filter(Patient.patient_id == Visit.patient_id)
            .order_by(Visit.visit_id))
    return [VisitChargePatient(visit=v, charge=c, patient=p) for (v, p, c) in rows]


def delete_duplicate_shinryou(session: Session, visit_id: int) -> List[int]:
    ss = session.query(Shinryou).filter_by(visit_id=visit_id).order_by(Shinryou.shinryou_id)
    codes: Set[int] = set()
    dups: List[Shinryou] = []
    for s in ss:
        if s.shinryoucode in codes:
            dups.append(s)
        else:
            codes.add(s.shinryoucode)
    for s in dups:
        session.delete(s)
    return [s.shinryou_id for s in dups]


def get_koukikourei(session: Session, koukikourei_id: int) -> Koukikourei:
    return session.query(Koukikourei).get(koukikourei_id)


def get_shinryou_byoumei_map_config_file_path():
    return SHINRYOU_BYOUMEI_MAP_FILE


def search_iyakuhin_master_by_name(session, text, at):
    if not text:
        return []
    at = _normalize_at(at)
    return (session.query(IyakuhinMaster)
            .filter(IyakuhinMaster.name.like(f"%{text}%"))
            .filter(_valid_at(IyakuhinMaster, at))
            .all())


def resolve_shinryou_master(session, shinryoucode, at):
    return _resolve_shinryou_master(session, shinryoucode, at)


def get_hokensho(patient_id: int, file: str) -> Dict:
    # noinspection PyTypeChecker
    file_path = os.path.join(PAPER_SCAN_DIR, str(patient_id), file)
    return {
        "filename_or_fp": file_path,
        "mimetype": "application/octet-stream",
        "as_attachment": True,
        "attachment_filename": file
    }


def delete_shinryou_tekiyou(session: Session, shinryou_id: int) -> bool:
    attr = session.query(ShinryouAttr).get(shinryou_id)
    if attr:
        attr.tekiyou = None
    return True


def search_text_by_page(session: Session, patient_id: int, text: str, page: int) -> TextVisitPage:
    q = (session.query(Text, Visit)
         .filter(Text.visit_id == Visit.visit_id)
         .filter(Visit.patient_id == patient_id)
         .filter(Text.content.like(f"%{text}%")))
    total = q.count()
    items_per_page = 20
    total_pages = _count_pages(total, items_per_page)
    rows = q.order_by(Text.text_id).offset(page * items_per_page).limit(items_per_page)
    return TextVisitPage(
        total_pages=total_pages,
        page=page,
        text_visits=[TextVisit(text=t, visit=v) for (t, v) in rows]
    )


def page_visit_drug(session: Session, patient_id: int, page: int) -> VisitDrugPage:
    items_per_page = 10
    q = (session.query(Visit)
         .join(Drug, Drug.visit_id == Visit.visit_id)
         .filter(Visit.patient_id == patient_id)
         .group_by(Visit.visit_id)
         .having(func.count(Drug.drug_id) > 0))
    total = q.count()
    total_pages = _count_pages(total, items_per_page)
    return VisitDrugPage(
        total_pages=total_pages,
        page=page,
        visit_drugs=[VisitDrug(
            visit=v,
            drugs=list_drug_full(session, v.visit_id)
        ) for v in q.order_by(Visit.visit_id.desc()).offset(page * items_per_page).limit(items_per_page)]
    )


def _list_conduct_drug_full(session, conduct_id):
    rows = (session.query(ConductDrug, IyakuhinMaster)
            .join(Conduct, Conduct.conduct_id == ConductDrug.conduct_id)
            .join(Visit, Visit.visit_id == Conduct.visit_id)
            .filter(ConductDrug.conduct_id == conduct_id)
            .filter(IyakuhinMaster.iyakuhincode == ConductDrug.iyakuhincode)
            .filter(IyakuhinMaster.valid_from <= func.date(Visit.visited_at))
            .filter(or_(IyakuhinMaster.valid_upto == ZERO_DATE,
                        func.date(Visit.visited_at) <= IyakuhinMaster.valid_upto))
            .order_by(ConductDrug.conduct_drug_id)
            .all())
    return [ConductDrugFull(conduct_drug=d, master=m) for (d, m) in rows]


def get_conduct_drug_full(session: Session, conduct_drug_id: int) -> ConductDrugFull:
    (d, m) = (session.query(ConductDrug, IyakuhinMaster)
              .join(Conduct, Conduct.conduct_id == ConductDrug.conduct_id)
              .join(Visit, Visit.visit_id == Conduct.visit_id)
              .filter(ConductDrug.conduct_drug_id == conduct_drug_id)
              .filter(IyakuhinMaster.iyakuhincode == ConductDrug.iyakuhincode)
              .filter(_valid_at(IyakuhinMaster, func.date(Visit.visited_at)))
              .one())
    return ConductDrugFull(conduct_drug=d, master=m)


def count_page_of_disease_by_patient(session: Session, patient_id: int, items_per_page: int) -> int:
    return _count_pages(session.query(Disease).filter_by(patient_id=patient_id).count(), items_per_page)


def _calc_rcpt_age(patient: Patient, visit: Visit) -> int:
    bd = _sqldate_to_date(patient.birthday)
    td = _sqldatetime_to_datetime(visit.visited_at)
    return rcpt.calc_rcpt_age(bd.year, bd.month, bd.day, td.year, td.month)


def get_visit_meisai(session: Session, visit_id: int) -> Meisai:
    visit = session.query(Visit).get(visit_id)
    at = _normalize_at(visit.visited_at)
    patient = session.query(Patient).get(visit.patient_id)
    rcpt_age = _calc_rcpt_age(patient, visit)
    hoken = _get_hoken_for_visit(session, visit)
    visit_full = _get_visit_full_2(session, visit)
    houkatsu_kensa = houkatsu.HoukatsuKensa.from_file(HOUKATSU_KENSA_FILE_PATH)
    revision = houkatsu_kensa.pick_revision(at)
    rcpt_visit = rcpt.RcptVisit()
    rcpt_visit.add_shinryou_list(visit_full.shinryou_list, revision)
    rcpt_visit.add_drugs(visit_full.drugs)
    rcpt_visit.add_conducts(visit_full.conducts)
    sections: List[MeisaiSection] = [sect for sect in rcpt_visit.meisai.get_sections() if sect.items]
    total_ten: int = sum(sect.section_total_ten for sect in sections)
    futan_wari: int = rcpt.calc_futan_wari(hoken, rcpt_age)
    charge: int = rcpt.calc_charge(total_ten, futan_wari)
    return Meisai(
        sections=sections,
        total_ten=total_ten,
        futan_wari=futan_wari,
        charge=charge,
        hoken=hoken
    )


def start_exam(session: Session, visit_id: int) -> bool:
    wq: Wqueue = session.query(Wqueue).get(visit_id)
    if wq:
        wq.wait_state = WqueueStateInExam
    return True


def get_shinryou_master(session: Session, shinryoucode: int, at) -> ShinryouMaster:
    at = _normalize_at(at)
    return (session.query(ShinryouMaster)
            .filter_by(shinryoucode=shinryoucode)
            .filter(_valid_at(ShinryouMaster, at))
            .one())


def _search_prev_drug_all(session, patient_id):
    drug_ids = (session.query(func.max(Drug.drug_id))
                .join(Visit, Visit.visit_id == Drug.visit_id)
                .filter(Visit.patient_id == patient_id)
                .filter(Drug.category.in_([DrugCategoryNaifuku, DrugCategoryTonpuku]))
                .group_by(Drug.iyakuhincode, Drug.amount, Drug.usage, Drug.days)
                .all())
    drug_ids += (session.query(func.max(Drug.drug_id))
                 .join(Visit, Visit.visit_id == Drug.visit_id)
                 .filter(Visit.patient_id == patient_id)
                 .filter(Drug.category == DrugCategoryGaiyou)
                 .group_by(Drug.iyakuhincode, Drug.amount, Drug.usage)
                 .all())
    drug_fulls = [get_drug_full(session, drug_id) for (drug_id,) in drug_ids]
    drug_fulls.sort(key=lambda x: (-x.drug.visit_id, x.drug.drug_id))
    return drug_fulls


def _search_prev_drug_by_name(session, patient_id, text):
    print("TEXT:", f"%{text}%")
    drug_ids = (session.query(func.max(Drug.drug_id))
                .join(Visit, Visit.visit_id == Drug.visit_id)
                .join(IyakuhinMaster, IyakuhinMaster.iyakuhincode == Drug.iyakuhincode)
                .filter(Visit.patient_id == patient_id)
                .filter(Drug.category.in_([DrugCategoryNaifuku, DrugCategoryTonpuku]))
                .filter(IyakuhinMaster.name.like(f"%{text}%"))
                .filter(IyakuhinMaster.valid_from <= func.date(Visit.visited_at))
                .filter(or_(IyakuhinMaster.valid_upto == "0000-00-00",
                            func.date(Visit.visited_at) <= IyakuhinMaster.valid_upto))
                .group_by(Drug.iyakuhincode, Drug.amount, Drug.usage, Drug.days)
                .all())
    drug_ids += (session.query(func.max(Drug.drug_id))
                 .join(Visit, Visit.visit_id == Drug.visit_id)
                 .join(IyakuhinMaster, IyakuhinMaster.iyakuhincode == Drug.iyakuhincode)
                 .filter(Visit.patient_id == patient_id)
                 .filter(Drug.category == DrugCategoryGaiyou)
                 .filter(IyakuhinMaster.name.like(f"%{text}%"))
                 .filter(IyakuhinMaster.valid_from <= func.date(Visit.visited_at))
                 .filter(or_(IyakuhinMaster.valid_upto == "0000-00-00",
                             func.date(Visit.visited_at) <= IyakuhinMaster.valid_upto))
                 .group_by(Drug.iyakuhincode, Drug.amount, Drug.usage)
                 .all())
    drug_fulls = [get_drug_full(session, drug_id) for (drug_id,) in drug_ids]
    drug_fulls.sort(key=lambda x: (-x.drug.visit_id, x.drug.drug_id))
    return drug_fulls


def search_prev_drug(session, text, patient_id):
    if not text:
        return _search_prev_drug_all(session, patient_id)
    else:
        return _search_prev_drug_by_name(session, patient_id, text)


def list_shinryou_full_by_ids(session, shinryou_ids):
    rows = (session.query(Shinryou, ShinryouMaster)
            .join(Visit, Visit.visit_id == Shinryou.visit_id)
            .filter(Shinryou.shinryou_id.in_(shinryou_ids))
            .filter(ShinryouMaster.shinryoucode == Shinryou.shinryoucode)
            .filter(ShinryouMaster.valid_from <= func.date(Visit.visited_at))
            .filter(or_(ShinryouMaster.valid_upto == ZERO_DATE,
                        func.date(Visit.visited_at) <= ShinryouMaster.valid_upto))
            .order_by(Shinryou.shinryoucode)
            .all())
    return [ShinryouFull(shinryou=s, master=m) for (s, m) in rows]


def start_visit(session: Session, patient_id: int, at) -> int:
    if not at:
        at = _now_as_sqldatetime()
    else:
        at = _normalize_datetime(at)
    visit = Visit(visit_id=None, patient_id=patient_id, visited_at=at)
    hoken = list_available_hoken(session, patient_id, at)
    visit.shahokokuho_id = hoken.shahokokuho.shahokokuho_id if hoken.shahokokuho else 0
    visit.koukikourei_id = hoken.koukikourei.koukikourei_id if hoken.koukikourei else 0
    visit.roujin_id = hoken.roujin.roujin_id if hoken.roujin else 0
    visit.kouhi_1_id = hoken.kouhi_1.kouhi_id if hoken.kouhi_1 else 0
    visit.kouhi_2_id = hoken.kouhi_2.kouhi_id if hoken.kouhi_2 else 0
    visit.kouhi_3_id = hoken.kouhi_3.kouhi_id if hoken.kouhi_3 else 0
    session.add(visit)
    session.flush()
    wq = Wqueue(visit_id=visit.visit_id, wait_state=WqueueStateWaitExam)
    session.add(wq)
    return visit.visit_id


def modify_disease(session: Session, disease_modify: DiseaseModify) -> bool:
    disease_id = disease_modify.disease.disease_id
    session.merge(disease_modify.disease)
    shuushokugocodes: List[int] = disease_modify.shuushokugocodes
    adj_list: List[DiseaseAdj] = (session.query(DiseaseAdj)
                                  .filter_by(disease_id=disease_id)
                                  .order_by(DiseaseAdj.disease_adj_id)
                                  .all())
    cur_shuushokugocodes: List[int] = [adj.shuushokugocode for adj in adj_list]
    if not shuushokugocodes == cur_shuushokugocodes:
        for adj in adj_list:
            session.delete(adj)
        for code in shuushokugocodes:
            new_adj = DiseaseAdj(disease_adj_id=None, disease_id=disease_id, shuushokugocode=code)
            session.add(new_adj)
    return True


def delete_shinryou(session, shinryou_id):
    shinryou = session.query(Shinryou).get(shinryou_id)
    session.delete(shinryou)
    return True


def list_visit_text_drug_for_patient(session: Session, patient_id: int, page: int) -> VisitTextDrugPage:
    items_per_page = 10
    order = Visit.visit_id.desc()
    q = (session.query(Visit).filter_by(patient_id=patient_id))
    total = q.count()
    total_pages = _count_pages(total, items_per_page)
    visits = q.order_by(order).offset(page * items_per_page).limit(items_per_page).all()
    return VisitTextDrugPage(
        total_pages=total_pages,
        page=page,
        visit_text_drugs=[VisitTextDrug(
            visit=v,
            texts=list_text(session, v.visit_id),
            drugs=list_drug_full(session, v.visit_id)
        ) for v in visits]
    )


def get_refer_list():
    return REFER_LIST


def end_exam(session: Session, visit_id: int, charge: int) -> bool:
    visit = session.query(Visit).get(visit_id)
    is_today = _normalize_at(visit.visited_at) == _today_as_sqldate()
    modify_charge(session, visit_id, charge)
    wq: Optional[Wqueue] = session.query(Wqueue).get(visit_id)
    if wq and is_today:
        wq.wait_state = WqueueStateWaitCashier
    else:
        if wq:
            session.delete(wq)
        new_wq = Wqueue(visit_id=visit_id, wait_state=WqueueStateWaitCashier)
        session.add(new_wq)
    pq = session.query(PharmaQueue).get(visit_id)
    if pq:
        session.delete(pq)
    if is_today:
        unprescribed = session.query(Drug).filter_by(visit_id=visit_id).filter(Drug.prescribed == 0).count()
        if unprescribed > 0:
            new_pq = PharmaQueue(visit_id=visit_id, pharma_state=PharmaQueueStateWaitPack)
            session.add(new_pq)
    return True


def search_kizai_master(session: Session, text: str, at) -> List[KizaiMaster]:
    at = _normalize_at(at)
    return (session.query(KizaiMaster)
            .filter(KizaiMaster.name.like(f"%{text}%"))
            .filter(_valid_at(KizaiMaster, at))
            .order_by(KizaiMaster.yomi)
            .all())


def batch_resolve_shuushokugo_names(session: Session, at, args: List[List[str]]) -> Dict[str, int]:
    # noinspection PyUnusedLocal
    at = _normalize_at(at)
    result: Dict[str, int] = {}
    for arg in args:
        if len(arg) == 0:
            continue
        name = arg[0]
        keys = arg[1:] if len(arg) > 1 else arg
        for key in keys:
            m = find_shuushokugo_master_by_name(session, key)
            if m:
                result[name] = m.shuushokugocode
                break
    return result


def batch_update_disease_end_reason(session: Session, args: List[DiseaseModifyEndReason]) -> bool:
    for arg in args:
        d = session.query(Disease).get(arg.disease_id)
        d.end_reason = arg.end_reason
        d.end_date = _normalize_at(arg.end_date)
    return True


def list_practice_log_in_range(session: Session, date, after_id: int, before_id: int) -> List[PracticeLog]:
    date = _normalize_at(date)
    return (session.query(PracticeLog)
            .filter(func.date(PracticeLog.created_at) == date)
            .filter(PracticeLog.serial_id > after_id)
            .filter(PracticeLog.serial_id < before_id)
            .order_by(PracticeLog.serial_id)
            .all())


def get_name_map_config_file_path() -> str:
    # noinspection PyTypeChecker
    return NAME_MAP_FILE_PATH


def get_hoken(session, visit_id):
    visit = get_visit(session, visit_id)
    return _get_hoken_for_visit(session, visit)


def update_kouhi(session: Session, kouhi: Kouhi) -> bool:
    session.merge(kouhi)
    return True


def suspend_exam(session, visit_id) -> bool:
    wq = session.query(Wqueue).get(visit_id)
    if wq:
        wq.wait_state = WqueueStateWaitReExam
    return True


def list_payment_by_patient(session, patient_id, n: Optional[int]) -> List[PaymentVisitPatient]:
    if n is None:
        n = 30
    order = Payment.visit_id.desc()
    rows = (session.query(Payment, Visit, Patient)
            .filter(Payment.visit_id == Visit.visit_id)
            .filter(Visit.patient_id == patient_id)
            .filter(Patient.patient_id == Visit.patient_id)
            .order_by(order)
            .limit(n))
    return [PaymentVisitPatient(payment=pay, visit=v, patient=p) for (pay, v, p) in rows]


def list_visiting_patient_id_having_hoken(session: Session, year: int, month: int) -> List[int]:
    rows = (session.query(distinct(Visit.patient_id))
            .filter(func.year(Visit.visited_at) == year)
            .filter(func.month(Visit.visited_at) == month)
            .filter(_having_hoken()))
    return [patient_id for patient_id, in rows]


def update_text(session, text):
    session.merge(text)


def resolve_kizai_master_by_name(session, name, at) -> Optional[KizaiMaster]:
    return _resolve_kizai_master_by_name(session, name, at)


def list_visit_id_by_patient(session, patient_id) -> List[int]:
    order = Visit.visit_id.desc()
    rows = session.query(Visit.visit_id).filter_by(patient_id=patient_id).order_by(order)
    return [visit_id for visit_id, in rows]


def get_pharma_drug(session, iyakuhincode):
    return session.query(PharmaDrug).get(iyakuhincode)


def batch_update_drug_days(session, drug_ids, days):
    for drug_id in drug_ids:
        drug = get_drug(session, drug_id)
        drug.days = days
    return True


def delete_drug(session, drug_id):
    drug = session.query(Drug).get(drug_id)
    session.delete(drug)
    return True


def _list_conduct_shinryou_full(session, conduct_id):
    rows = (session.query(ConductShinryou, ShinryouMaster)
            .join(Conduct, Conduct.conduct_id == ConductShinryou.conduct_id)
            .join(Visit, Visit.visit_id == Conduct.visit_id)
            .filter(ConductShinryou.conduct_id == conduct_id)
            .filter(ConductShinryou.shinryoucode == ShinryouMaster.shinryoucode)
            .filter(ShinryouMaster.valid_from <= func.date(Visit.visited_at))
            .filter(or_(ShinryouMaster.valid_upto == ZERO_DATE,
                        func.date(Visit.visited_at) <= ShinryouMaster.valid_upto))
            .order_by(ConductShinryou.conduct_shinryou_id)
            .all())
    return [ConductShinryouFull(conduct_shinryou=c, master=m) for (c, m) in rows]


def get_conduct_shinryou_full(session, conduct_shinryou_id):
    (c, m) = (session.query(ConductShinryou, ShinryouMaster)
              .join(Conduct, ConductShinryou.conduct_id == Conduct.conduct_id)
              .join(Visit, Visit.visit_id == Conduct.visit_id)
              .filter(ConductShinryou.conduct_shinryou_id == conduct_shinryou_id)
              .filter(ConductShinryou.shinryoucode == ShinryouMaster.shinryoucode)
              .filter(ShinryouMaster.valid_from <= func.date(Visit.visited_at))
              .filter(or_(ShinryouMaster.valid_upto == ZERO_DATE,
                          func.date(Visit.visited_at) <= ShinryouMaster.valid_upto))
              .order_by(ConductShinryou.conduct_shinryou_id)
              .one())
    return ConductShinryouFull(conduct_shinryou=c, master=m)


def enter_conduct_drug(session, conduct_drug: ConductDrug) -> int:
    conduct_drug.conduct_drug_id = None
    session.add(conduct_drug)
    session.flush()
    # noinspection PyTypeChecker
    return conduct_drug.conduct_drug_id


def _delete_visit_safely(session, visit_id) -> None:
    if session.query(Text).filter_by(visit_id=visit_id).count() > 0:
        raise Exception("文章があるので、診察を削除できません。")
    if session.query(Drug).filter_by(visit_id=visit_id).count() > 0:
        raise Exception("投薬があるので、診察を削除できません。")
    if session.query(Shinryou).filter_by(visit_id=visit_id).count() > 0:
        raise Exception("診療行為があるので、診察を削除できません。")
    if session.query(Conduct).filter_by(visit_id=visit_id).count() > 0:
        raise Exception("処置があるので、診察を削除できません。")
    if session.query(Charge).filter_by(visit_id=visit_id).count() > 0:
        raise Exception("請求があるので、診察を削除できません。")
    if session.query(Payment).filter_by(visit_id=visit_id).count() > 0:
        raise Exception("支払い記録があるので、診察を削除できません。")
    wq = session.query(Wqueue).get(visit_id)
    if wq:
        session.delete(wq)
    pq = session.query(PharmaQueue).get(visit_id)
    if pq:
        session.delete(pq)
    visit = session.query(Visit).get(visit_id)
    if visit:
        session.delete(visit)


def delete_visit_from_reception(session, visit_id) -> bool:
    wq = session.query(Wqueue).get(visit_id)
    if wq and wq.waite_state != WqueueStateWaitExam:
        raise Exception("診察の状態が診察待ちでないため、削除できません。")
    _delete_visit_safely(session, visit_id)
    return True


def copy_all_conducts(session, target_visit_id, source_visit_id) -> List[int]:
    new_conduct_ids = []
    src_conducts = session.query(Conduct).filter_by(visit_id=source_visit_id)
    target_visit = session.query(Visit).get(target_visit_id)
    target_at = _normalize_at(target_visit.visited_at)
    for src_conduct in src_conducts:
        src_conduct_id = src_conduct.conduct_id
        new_conduct = Conduct(conduct_id=None, visit_id=target_visit_id, kind=src_conduct.kind)
        session.add(new_conduct)
        session.flush()
        new_conduct_id = new_conduct.conduct_id
        new_conduct_ids.append(new_conduct_id)
        for shinryou in session.query(ConductShinryou).filter_by(conduct_id=src_conduct_id):
            m = resolve_shinryou_master(session, shinryou.shinryoucode, target_at)
            if not m:
                raise Exception(f"診療行為を追加できません。")
            new_shinryou = ConductShinryou(
                conduct_shinryou_id=None,
                conduct_id=new_conduct_id,
                shinryoucode=m.shinryoucode
            )
            session.add(new_shinryou)
        for drug in session.query(ConductDrug).filter_by(conduct_id=src_conduct_id):
            m = resolve_iyakuhin_master(session, drug.iyakuhincode, target_at)
            if not m:
                raise Exception(f"医薬品を追加できません。")
            new_drug = ConductDrug(
                conduct_drug_id=None,
                conduct_id=new_conduct_id,
                iyakuhincode=m.iyakuhincode,
                amount=drug.amount
            )
            session.add(new_drug)
        for kizai in session.query(ConductKizai).filter_by(conduct_id=src_conduct_id):
            m = resolve_kizai_master(session, kizai.iyakuhincode, target_at)
            if not m:
                raise Exception(f"器材を追加できません。")
            new_kizai = ConductKizai(
                conduct_kizai_id=None,
                conduct_id=new_conduct_id,
                kizaicode=m.kizaicode,
                amount=kizai.amount
            )
            session.add(new_kizai)
    return new_conduct_ids


def enter_presc_example(session, presc_example: PrescExample) -> int:
    presc_example.presc_example_id = None
    session.add(presc_example)
    # noinspection PyTypeChecker
    return presc_example.presc_example_id


def delete_presc_example(session, presc_example_id) -> bool:
    e = session.query(PrescExample).get(presc_example_id)
    if e:
        session.delete(e)
    return True


def find_shuushokugo_master_by_name(session: Session, name: str) -> Optional[ShuushokugoMaster]:
    return session.query(ShuushokugoMaster).filter_by(name=name).one_or_none()


def get_name_of_iyakuhin(session, iyakuhincode) -> Optional[str]:
    row = (session.query(IyakuhinMaster.name)
           .filter_by(iyakuhincode=iyakuhincode)
           .order_by(IyakuhinMaster.valid_from.desc())
           .one_or_none())
    return row[0] if row else None


def set_shinryou_tekiyou(session, shinryou_id, tekiyou: str) -> ShinryouAttr:
    attr = session.query(ShinryouAttr).get(shinryou_id)
    if attr:
        attr.tekiyou = tekiyou
    else:
        attr = ShinryouAttr(shinryou_id=shinryou_id, tekiyou=tekiyou)
        session.add(attr)
        session.flush()
    return attr


def get_visit(session, visit_id):
    return session.query(Visit).get(visit_id)


def modify_gazou_label(session, conduct_id, label: str) -> bool:
    gazou = session.query(GazouLabel).get(conduct_id)
    if gazou:
        gazou.label = label
    else:
        gazou = GazouLabel(conduct_id=conduct_id, label=label)
        session.add(gazou)
    return True


def update_pharma_drug(session, pharma_drug: PharmaDrug) -> bool:
    session.merge(pharma_drug)
    return True


def get_powder_drug_config_file_path() -> str:
    # noinspection PyTypeChecker
    return POWDER_DRUG_FILE_PATH


def list_recent_hotline(session, threshold_hotline_id) -> List[Hotline]:
    return (session.query(Hotline)
            .filter(Hotline.hotline_id > threshold_hotline_id)
            .order_by(Hotline.hotline_id)
            .all())


def list_text(session, visit_id) -> List[Text]:
    return (session.query(Text)
            .filter_by(visit_id=visit_id)
            .order_by(Text.text_id)
            .all())


def get_roujin(session, roujin_id) -> Optional[Roujin]:
    return session.query(Roujin).get(roujin_id)


def list_all_practice_log(session, date, last_id) -> List[PracticeLog]:
    at = _normalize_at(date)
    return (session.query(PracticeLog)
            .filter(func.date(PracticeLog.created_at) == at)
            .filter(PracticeLog.serial_id > last_id)
            .order_by(PracticeLog.serial_id)
            .all())


def list_recent_payment(session, n: Optional[int]) -> List[PaymentVisitPatient]:
    if n is None:
        n = 30
    rows = (session.query(Payment, Visit, Patient)
            .filter(Payment.visit_id == Visit.visit_id)
            .filter(Patient.patient_id == Visit.patient_id)
            .order_by(Payment.visit_id.desc())
            .limit(n))
    return [PaymentVisitPatient(payment=pay, visit=v, patient=p) for (pay, v, p) in rows]


def batch_resolve_kizai_names(session, at, args: List[List[str]]) -> Dict[str, int]:
    def resolver(arg_session, arg_name, arg_at):
        master = _find_kizai_master_by_name(arg_session, arg_name, arg_at)
        return master.kizaicode if master else None

    return _batch_resolve_names(session, resolver, at, args)


def list_todays_hotline(session) -> List[Hotline]:
    today = _today_as_sqldate()
    return (session.query(Hotline)
            .filter(func.date(Hotline.posted_at) == today)
            .order_by(Hotline.hotline_id)
            .all())


def find_todays_last_hotline(session) -> Optional[Hotline]:
    today = _today_as_sqldate()
    return (session.query(Hotline)
            .filter(func.date(Hotline.posted_at) == today)
            .order_by(Hotline.hotline_id.desc())
            .first())


def find_todays_last_practice_log(session) -> Optional[PracticeLog]:
    today = _today_as_sqldate()
    return (session.query(PracticeLog)
            .filter(func.date(PracticeLog.created_at) == today)
            .order_by(PracticeLog.serial_id.desc())
            .first())


def resolve_shinryou_master_by_name(session, name, at) -> Optional[ShinryouMaster]:
    return _resolve_shinryou_master_by_name(session, name, at)


def enter_xp(session: Session, visit_id: int, label: str, film: str) -> int:
    conduct = Conduct(conduct_id=None, visit_id=visit_id, kind=ConductKindGazou)
    session.add(conduct)
    session.flush()
    conduct_id = conduct.conduct_id
    _enter_gazou_label(session, conduct_id, label)
    _enter_conduct_shinryou_by_name(session, conduct_id, "単純撮影")
    _enter_conduct_shinryou_by_name(session, conduct_id, "単純撮影診断")
    _enter_conduct_kiazi_by_name(session, conduct_id, film, 1)
    return conduct_id


def enter_shahokokuho(session, shahokokuho: Shahokokuho) -> int:
    shahokokuho.shahokokuho_id = None
    session.add(shahokokuho)
    session.flush()
    # noinspection PyTypeChecker
    return shahokokuho.shahokokuho_id


def update_presc_example(session, presc_example: PrescExample) -> bool:
    session.merge(presc_example)
    return True


def get_practice_config():
    return PRACTICE_CONFIG


def modify_conduct_kind(session, conduct_id: int, kind: int) -> bool:
    conduct = session.query(Conduct).get(conduct_id)
    if conduct:
        conduct.kind = kind
    return True


def enter_patient(session: Session, patient: Patient) -> int:
    patient.patient_id = None
    session.add(patient)
    session.flush()
    # noinspection PyTypeChecker
    return patient.patient_id


def page_visit_full_with_patient_at(session: Session, at: Union[str, datetime.datetime, datetime.date],
                                    page: int) -> VisitFull2PatientPage:
    at = _normalize_at(at)
    order = Visit.visit_id.desc()
    items_per_page = 10
    q = (session.query(Visit, Patient)
         .filter(func.date(Visit.visited_at) == at)
         .filter(Patient.patient_id == Visit.patient_id))
    total = q.count()
    total_pages = _count_pages(total, items_per_page)
    visits = q.order_by(order).offset(page * items_per_page).limit(items_per_page)
    return VisitFull2PatientPage(
        total_pages=total_pages,
        page=page,
        visit_patients=[VisitFull2Patient(
            patient=p,
            visit_full=_get_visit_full_2(session, v)
        ) for v, p in visits]
    )


def update_shahokokuho(session: Session, shahokokuho: Shahokokuho) -> bool:
    session.merge(shahokokuho)
    return True


def enter_text(session, text):
    text.text_id = None
    session.add(text)
    session.flush()
    return text.text_id


def delete_visit(session, visit_id) -> bool:
    _delete_visit_safely(session, visit_id)
    return True


def get_disease_full(session: Session, disease_id: int) -> DiseaseFull:
    (d, m) = (session.query(Disease, ByoumeiMaster)
              .filter(Disease.disease_id == disease_id)
              .filter(ByoumeiMaster.shoubyoumeicode == Disease.shoubyoumeicode)
              .filter(_valid_at(ByoumeiMaster, Disease.start_date))
              .one())
    return DiseaseFull(disease=d, master=m, adj_list=_list_disease_adj_full(session, d.disease_id))


