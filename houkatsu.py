import xml.etree.ElementTree as ETree
from typing import Dict, Optional, Union
import datetime


class Step:
    def __init__(self, thresh: int, point: int):
        self.thresh = thresh
        self.point = point


class Group:
    def __init__(self):
        self.steps = []

    def add(self, step: Step):
        self.steps.append(step)

    def calc_ten(self, n: int) -> Optional[int]:
        for s in self.steps:
            if s.thresh <= n:
                return s.point
        return None


class Revision:
    def __init__(self, valid_from: str):
        self.valid_from = valid_from
        self.group: Dict[str, Group] = {}

    def add(self, key, group):
        self.group[key] = group

    def calc_ten(self, key, n: int) -> Optional[int]:
        g = self.group.get(key)
        if g:
            return g.calc_ten(n)
        else:
            return None


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


class HoukatsuKensa:
    def __init__(self):
        self.revisions = []

    def add(self, revision: Revision):
        self.revisions.append(revision)

    def pick_revision(self, at) -> Optional[Revision]:
        for r in self.revisions:
            if r.valid_from <= at:
                return r
        return None

    @staticmethod
    def from_file(file):
        root = ETree.parse(file).getroot()
        houkatsu = HoukatsuKensa()
        for xml_rev in root.find("revisions"):
            valid_from = xml_rev.attrib["valid-from"]
            rev = Revision(valid_from)
            xml_groups = xml_rev.find("groups")
            for xml_group in xml_groups:
                key = xml_group.attrib["key"]
                group = Group()
                for xml_step in xml_group.findall("step"):
                    thresh = int(xml_step.find("threshold").text.strip())
                    point = int(xml_step.find("point").text.strip())
                    step = Step(thresh, point)
                    group.add(step)
                rev.add(key, group)
            houkatsu.add(rev)
        return houkatsu
