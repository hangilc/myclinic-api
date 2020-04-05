from typing import List, Optional

from server_app import Session
import impl
from model import Visit, Meisai, MeisaiSection, SectionItem
import random
import signal
import sys
import requests
from itertools import chain
import consts
import json


def rand_gen(start, upto):
    stop = upto + 1
    while True:
        yield random.randrange(start, stop)


def rand_gen_seq(upper):
    while upper >= 1:
        yield upper
        upper -= 1


def find_section(section_name: str, sections: List[MeisaiSection]) -> Optional[MeisaiSection]:
    for sect in sections:
        if sect.name == section_name:
            return sect
    return None


def print_section_items(prefix: str, items: List[SectionItem]) -> None:
    for item in items:
        print(f"{prefix}: {item.tanka} {item.count} {item.label}")


def spot_difference(visit: Visit, a: Meisai, b: Meisai) -> None:
    print(f"Meisai mismatch at visit_id {visit.visit_id}, patient_id {visit.patient_id}, visited_at {visit.visited_at}")
    visit_id = visit.visit_id
    if a.total_ten != b.total_ten:
        print(f"total_ten different {a.total_ten} - {b.total_ten}")
    if a.futan_wari != b.futan_wari:
        print(f"futan_wari different {a.futan_wari} - {b.futan_wari}")
    if a.charge != b.charge:
        print(f"charge different {a.charge} - {b.charge}")
    for sect_name in [sect.ident for sect in consts.MeisaiSections]:
        sa = find_section(sect_name, a.sections)
        sb = find_section(sect_name, b.sections)
        if sa is None and sb is None:
            continue
        if sa is None:
            print("A", "missing")
            print_section_items("B", sb.items)
            continue
        if sb is None:
            print_section_items("A", sa.items)
            print("B", "missing")
            continue
        if sa.section_total_ten != sb.section_total_ten:
            print(f"section {sa.label} is different")
            sa_tens = set(item.tanka * item.count for item in sa.items)
            sb_tens = set(item.tanka * item.count for item in sb.items)
            sa_diff = sa_tens - sb_tens
            for item in sa.items:
                ten = item.tanka * item.count
                if ten in sa_diff:
                    print(f"A: {item.tanka} {item.count} {item.label}")
            sb_diff = sb_tens - sa_tens
            for item in sb.items:
                ten = item.tanka * item.count
                if ten in sb_diff:
                    print(f"B: {item.tanka} {item.count} {item.label}")
            print("A FULL")
            shinryou_full = requests.get(f"http://localhost:18080/json/get-shinryou-full?visit-id={visit_id}").json()
            print(json.dumps(shinryou_full, indent=4))
            drug_full = requests.get(f"http://localhost:18080/json/get-drug-full?visit-id={visit_id}").json()
            print(json.dumps(drug_full, indent=4))
            conducts = requests.get("http://localhost:18080/json/")
            print("B FULL")
            visit_full = impl._get_visit_full_2(session, visit)
            print(json.dumps(visit_full.to_dict(), indent=4, ensure_ascii=False))


def run(gen):
    for visit_id in gen:
        visit = impl.get_visit(session, visit_id)
        if visit:
            print(f"Checking visit_id {visit_id}, patient_id: {visit.patient_id}, at: {visit.visited_at}")
            r = requests.get(f"http://localhost:18080/json/get-visit-meisai?visit-id={visit.visit_id}")
            r_meisai = Meisai.from_dict(r.json())
            r_total_ten = r_meisai.total_ten
            r_futan_wari = r_meisai.futan_wari
            r_charge = r_meisai.charge
            meisai = impl.get_visit_meisai(session, visit_id)
            total_ten = meisai.total_ten
            futan_wari = meisai.futan_wari
            charge = meisai.charge
            print(f"{visit_id} {r_total_ten} {r_futan_wari} {r_charge}")
            if total_ten == r_total_ten and futan_wari == r_futan_wari and charge == r_charge:
                print(f"{visit_id} OK")
            else:
                spot_difference(visit, r_meisai, meisai)
                sys.exit(1)


def run_random(pre, last_visit_id):
    run(chain(pre, rand_gen(1, last_visit_id)))


def run_seq(last_visit_id):
    run(rand_gen_seq(last_visit_id))


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, _: sys.exit(0))
    session = Session()
    last_visit_id = session.query(Visit.visit_id).order_by(Visit.visit_id.desc()).limit(1).scalar()
    # run_random(pre = [846, 15867, 74911, 36252], last_visit_id=last_visit_id)
    run_seq(last_visit_id)
