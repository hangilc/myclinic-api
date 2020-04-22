import os
from typing import List, Dict
import re


def remove_u3000_blank(s: str) -> str:
    return s.replace("\u3000", "")


class Pharmacy:
    def __init__(self, name, fax, addr):
        self.name = remove_u3000_blank(name)
        self.fax = fax
        self.addr = addr[0], remove_u3000_blank(addr[1])

    def __repr__(self):
        return f"<Pharmacy name={self.name}, fax={self.fax}, addr={self.addr}>"

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "fax": self.fax,
            "addr": self.addr
        }

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(
            d["name"],
            d["fax"],
            d["addr"]
        )


def pharmacy_list_file():
    return os.getenv("MYCLINIC_PHARMACY_LIST")


re_title = re.compile(r'【(.+)】')
re_fax = re.compile(r'fax:\s*(\+\d+)')
re_addr = re.compile(r'〒(\d{3}-\d{4})\s+(.+)')


def read_pharmacy_list(path: str) -> List[Pharmacy]:
    result = []
    name = None
    fax = None
    addr = None

    def flush():
        nonlocal name, fax, addr
        if name and fax and addr:
            result.append(Pharmacy(name, fax, addr))
        name = None
        fax = None
        addr = None

    with open(path, "r", encoding="UTF-8") as fp:
        for line in fp:
            line = line.strip()
            if not line:
                continue
            m = re_title.match(line)
            if m:
                flush()
                name = m.group(1)
                continue
            m = re_fax.match(line)
            if m:
                fax = m.group(1)
                continue
            m = re_addr.match(line)
            if m:
                addr = (m.group(1), m.group(2))
                continue
    flush()
    return result


def get_pharmacy_list():
    return read_pharmacy_list(pharmacy_list_file())


pharma_addr_map = {
    "+81333916310": "〒167-0051\n杉並区荻窪二丁目２０番４号\nオノダ薬局 御中",
    "+81353700250": "〒168-0081\n杉並区宮前一丁目２０番２９号\nスギ薬局高井戸店 御中",
    "+81353479268": "〒167-0051\n杉並区荻窪一丁目３３番１１号\n荻窪グレイスマンション１階\nすみれ薬局 御中",
    "+81353472576": "〒167-0051\n杉並区荻窪5丁目28番13号\nココカラファイン\n荻窪南仲通り店 御中",
    "+81333910268": "〒167-0051\n杉並区荻窪５丁目３０−１２\nグローリアビル1F\nクロダ薬局 御中",
    "+81353701215": "〒168-0081\n杉並区宮前四丁目24番18号\nスギ薬局杉並宮前店 御中",
    "+81353474611": "〒167-0051\n杉並区荻窪５丁目２７−５\n中島第二ビル 1階\n日本調剤荻窪薬局 御中",
    "+81353474051": "〒167-0051\n杉並区荻窪五丁目２６番７号\nセドナ薬局 御中",
    "+81333917621": "〒167-0051\n杉並区荻窪五丁目１８番７号\n明弘堂薬局 御中",
    "+81359419502": "〒167-0052\n杉並区南荻窪二丁目12番3号\nセンター薬局南荻窪店 御中",
    "+81353356204": "〒167-0051\n杉並区荻窪五丁目１番９号\nユニパリス南荻窪１階\nスミレ薬局 御中",
    "+81353979402": "〒167-0043\n杉並区上荻１丁目９−１\n荻窪タウンセブンビル\nココカラファイン\n荻窪北口店 御中",
    "+81333911193": "〒167-0051\n杉並区荻窪五丁目29番17号101号\nクロダ薬局支店 御中",
    "+81353356465": "〒167-0032\n杉並区天沼3-3-4 魚耕ビル\nココカラファイン薬局\n荻窪天沼店 御中",
    "+81353474199": "〒167-0051\n杉並区荻窪五丁目２１番１６号\nナチュラルローソン\nクオール薬局荻窪５丁目店 御中",
    "+81353649086": "〒166-0001\n杉並区阿佐谷北一丁目３番８号\n城西阿佐ヶ谷ビル１階\nなないろ薬局\nあさがや２号店 御中",
    "+81353389440": "〒161-0034\n新宿区上落合3-8-25\n調剤薬局ツルハドラッグ\n新宿上落合店 御中",
    "+81333334397": "〒168-0081\n杉並区宮前二丁目２１番１５号\n日本堂宮前薬局 御中",
    "+81333998005": "〒167-0042\n杉並区西荻北三丁目１８番２号\nメインステージ西荻窪駅前１０１\nとくだ薬局 御中",
    "+81333290906": "〒168-0065\n杉並区浜田山三丁目３１番５号\n日本堂伊藤薬局 御中"
}

if __name__ == "__main__":
    for pharmacy_entry in get_pharmacy_list():
        print(pharmacy_entry)
