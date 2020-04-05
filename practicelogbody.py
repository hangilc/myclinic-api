from model import *
import json

_class_name_map = {
    'ByoumeiMaster': ByoumeiMaster,
    'Charge': Charge,
    'ConductDrug': ConductDrug,
    'Conduct': Conduct,
    'ConductKizai': ConductKizai,
    'ConductShinryou': ConductShinryou,
    'DiseaseAdj': DiseaseAdj,
    'Disease': Disease,
    'DrugAttr': DrugAttr,
    'Drug': Drug,
    'GazouLabel': GazouLabel,
    'Hotline': Hotline,
    'IntraclinicComment': IntraclinicComment,
    'IntraclinicPost': IntraclinicPost,
    'IntraclinicTag': IntraclinicTag,
    'IyakuhinMaster': IyakuhinMaster,
    'KizaiMaster': KizaiMaster,
    'Kouhi': Kouhi,
    'Koukikourei': Koukikourei,
    'Patient': Patient,
    'Payment': Payment,
    'PharmaDrug': PharmaDrug,
    'PharmaQueue': PharmaQueue,
    'PracticeLog': PracticeLog,
    'PrescExample': PrescExample,
    'Roujin': Roujin,
    'Shahokokuho': Shahokokuho,
    'ShinryouAttr': ShinryouAttr,
    'Shinryou': Shinryou,
    'ShinryouMaster': ShinryouMaster,
    'Shouki': Shouki,
    'ShuushokugoMaster': ShuushokugoMaster,
    'Text': Text,
    'Visit': Visit,
    'Wqueue': Wqueue,
}


def _hyphen_to_pascal(s):
    parts = s.split("-")
    return "".join([x.title() for x in parts])


class Created:
    def __init__(self, created):
        self.created = created

    def __repr__(self):
        return f"<Created(created={self.created})?"


class Updated:
    def __init__(self, updated):
        self.updated = updated


class Deleted:
    def __init__(self, deleted):
        self.deleted = deleted


def parse_body(plog: PracticeLog):
    kind = plog.kind
    body = json.loads(plog.body)
    if kind.endswith("-created"):
        cls = _hyphen_to_pascal(kind.replace("-created", ""))
        c = _class_name_map[cls]
        return Created(c.from_dict(body["created"]))
    elif kind.endswith("-updated"):
        cls = _hyphen_to_pascal(kind.replace("-updated", ""))
        c = _class_name_map[cls]
        return Updated(c.from_dict(body["updated"]))
    elif kind.endswith("-deleted"):
        cls = _hyphen_to_pascal(kind.replace("-deleted", ""))
        c = _class_name_map[cls]
        return Updated(c.from_dict(body["deleted"]))


if __name__ == "__main__":
    with open("java/dto.json", "r") as f:
        specs = json.load(f)
    for spec in specs:
        if spec.get("mysqlTable"):
            name = spec["name"]
            print(f"    '{name}': {name},")
