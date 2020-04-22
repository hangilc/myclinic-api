import datetime


class Gengou:
    def __init__(self, start_date, kanji, ident):
        self.ident = ident
        self.kanji = kanji
        self.start_date = start_date

    def __repr__(self):
        return self.kanji


Reiwa = Gengou(datetime.date(2019, 5, 1), "令和", "Reiwa")
Heisei = Gengou(datetime.date(1989, 1, 8), "平成", "Heisei")
Shouwa = Gengou(datetime.date(1926, 12, 25), "昭和", "Shouwa")
Taishou = Gengou(datetime.date(1912, 7, 30), "大正", "Taishou")
Meiji = Gengou(datetime.date(1873, 1, 1), "明治", "Meiji")
Seireki = Gengou(datetime.date(1, 1, 1), "西暦", "Seireki")

gengou_list = [Reiwa, Heisei, Shouwa, Taishou, Meiji]


def date_to_gengou(d: datetime.date) -> (Gengou, int):
    geng = Seireki
    for g in gengou_list:
        if d >= g.start_date:
            geng = g
            break
    return geng, d.year - geng.start_date.year + 1


def str_to_gengou(gengou: str) -> Gengou:
    for g in gengou_list:
        if g.ident == gengou or g.kanji == gengou:
            return g


def gengou_to_seireki(gengou, nen: int) -> int:
    if isinstance(gengou, str):
        gengou = str_to_gengou(gengou)
    return gengou.start_date.year + nen - 1



