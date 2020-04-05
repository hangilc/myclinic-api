from typing import List, Optional

from db_session import Session
from sqlalchemy.sql import func
from model import *
import datetime


def date_to_sqldate(d: datetime.date) -> str:
    return d.strftime("%Y-%m-%d")


today = datetime.date.today()
upto_date = today - datetime.timedelta(weeks=3)
from_date = today - datetime.timedelta(weeks=12)
upto_date_sql = date_to_sqldate(upto_date)
from_date_sql = date_to_sqldate(from_date)


class VisitData:
    def __init__(self, visit: Visit):
        self.visit = visit


class PatientData:
    def __init__(self, patient: Patient, limit_date: datetime.date):
        self.patient = patient
        self.limit_date = limit_date

    def update_limit_date(self, limit_date: datetime.date) -> None:
        if limit_date > self.limit_date:
            self.limit_date = limit_date


def is_presc(text: str) -> bool:
    return text.startswith("院外処方") or "Ｒｐ）" in text


re_presc_item_prefix = re.compile(r'\d+[)）]')
re_presc_days = re.compile(r'(\d+)\s*日分')
zenkaku_trans = str.maketrans("""０１２３４５６７８９　。．""", """0123456789 ..""")


def zenkaku_to_alpha(src: str) -> str:
    return src.translate(zenkaku_trans)


def extract_presc_items(text: str) -> List[str]:
    text = text.strip()
    items = []
    cur = ""
    for line in text.splitlines():
        line = zenkaku_to_alpha(line)
        if re_presc_item_prefix.match(line):
            if cur:
                items.append(cur)
            cur = line
        else:
            if cur:
                cur += line
    return items


def extract_days(text: str) -> Optional[int]:
    m = re_presc_days.search(text)
    if m:
        return int(m.group(1))
    else:
        return None


def presc_until(visit: Visit, days: int) -> datetime.date:
    d = visit.visited_at + datetime.timedelta(days=days)
    return d.date()


def run():
    session = Session()
    visits = (session.query(Visit)
              .filter(func.date(Visit.visited_at) >= from_date_sql)
              .filter(func.date(Visit.visited_at) <= upto_date_sql))
    patient_map = {}
    for visit in visits:
        texts = session.query(Text).filter_by(visit_id=visit.visit_id)
        for text in texts:
            if is_presc(text.content):
                items = extract_presc_items(text.content)
                days_items = [(extract_days(item), item) for item in items]
                regulars = [(presc_until(visit, days), days, item)
                            for days, item in days_items if days and days >= 28]
                if regulars:
                    reg_days = min(limit_day for limit_day, _, _ in regulars)
                    if visit.patient_id not in patient_map:
                        patient = session.query(Patient).get(visit.patient_id)
                        patient_map[patient.patient_id] = PatientData(patient, reg_days)
                    else:
                        patient_map[visit.patient_id].update_limit_date(reg_days)
    result = sorted(patient_map.values(), key=lambda d: d.limit_date)
    for d in result:
        print(f"{d.patient.last_name}{d.patient.first_name}, {d.patient.patient_id}, {d.limit_date}")


if __name__ == "__main__":
    run()
