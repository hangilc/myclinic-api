from typing import List, Union, Optional, Tuple
import datetime
from db_session import Session
from model import *
from sqlalchemy.sql import func
import re


def ensure_date(at: Union[str, datetime.datetime, datetime.date]) -> str:
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
    dfrom = ensure_date(date_from)
    dupto = ensure_date(date_upto)
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


def run(from_date, upto_date):
    session = Session()
    visits = list_visit(session, from_date, upto_date)
    for v in visits:
        print(v)
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
                presc = opt_presc
                presc_hit = True
            elif presc_hit:
                print(t.content)
                opt_pharma = probe_pharma(t.content)
                print(opt_pharma)
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
                pass
            elif hand_over:
                pass
            elif mail:
                pass
            elif fax_home:
                pass
            elif physical_mail:
                pass
            else:
                raise Exception(f"presc without pharma {v}")


if __name__ == "__main__":
    run("2020-03-26", "2020-04-11")
