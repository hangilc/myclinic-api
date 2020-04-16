import sys
from typing import List, Dict, Any
import math
from model import *
import houkatsu
import consts
from consts import MeisaiSectionComponent


class SectionItemEx(SectionItem):
    def __init__(self):
        super().__init__(count=1)
        self.merge_key = None


class SimpleShinryouSectionEx(SectionItemEx):
    def __init__(self, master: ShinryouMaster):
        super().__init__()
        self.tanka = shinryou_master_ten(master)
        self.label = master.name
        self.merge_key = ('simple-shinryou', master.shinryoucode)


class HoukatsuKensaSectionEx(SectionItemEx):
    def __init__(self, houkatsu_code: str, revision: houkatsu.Revision):
        super().__init__()
        self.houkatsu_code = houkatsu_code
        self.revision = revision
        self.masters: List[ShinryouMaster] = []

    def add(self, master: ShinryouMaster) -> None:
        self.masters.append(master)

    def update(self):
        t = None
        if self.revision:
            t = self.revision.calc_ten(self.houkatsu_code, len(self.masters))
        if t is None:
            t = sum(shinryou_master_ten(m) for m in self.masters)
        self.tanka = t
        self.label = "、".join(m.name for m in self.masters)
        self.merge_key = ('houkatsu-kensa', tuple(m.shinryoucode for m in self.masters))


def naifuku_extend_key(drug: Drug):
    usage = drug.usage.replace("就寝前", "寝る前")
    return usage, drug.days


class NaifukuSectionItemEx(SectionItemEx):
    def __init__(self, drug: DrugFull):
        super().__init__()
        self.extend_key = naifuku_extend_key(drug.drug)
        self.drugs: List[DrugFull] = [drug]
        self.count = drug.drug.days

    def add(self, drug: DrugFull) -> None:
        self.drugs.append(drug)

    def update(self):
        kingaku = sum(d.master.yakka * d.drug.amount for d in self.drugs)
        self.tanka = touyaku_kingaku_to_ten(kingaku)
        lbls = (f"{d.master.name} {d.drug.amount: g}{d.master.unit}" for d in self.drugs)
        self.label = "、".join(lbls)
        merges = ((d.master.iyakuhincode, d.drug.amount) for d in self.drugs)
        self.merge_key = 'naifuku', self.extend_key, tuple(merges)


class TonpukuSectionItemEx(SectionItemEx):
    def __init__(self, drug: DrugFull):
        super().__init__()
        self.tanka = touyaku_kingaku_to_ten(drug.master.yakka * drug.drug.amount)
        self.count = drug.drug.days
        self.label = f"{drug.master.name} {drug.drug.amount: g}{drug.master.unit}"
        self.merge_key = 'tonpuku', drug.master.iyakuhincode, drug.drug.usage, drug.drug.amount


class GaiyouSectionItemEx(SectionItemEx):
    def __init__(self, drug: DrugFull):
        super().__init__()
        self.tanka = touyaku_kingaku_to_ten((drug.master.yakka * drug.drug.amount))
        self.label = f"{drug.master.name} {drug.drug.amount: g}{drug.master.unit}"
        self.merge_key = "gaiyou", drug.master.iyakuhincode, drug.drug.usage, drug.drug.amount


class ConductDrugSectionItemEx(SectionItemEx):
    def __init__(self, sect: str, drug: ConductDrugFull):
        super().__init__()
        kingaku = drug.master.yakka * drug.conduct_drug.amount
        if sect == consts.MeisaiSectionGazou:
            self.tanka = shochi_kingaku_ten(kingaku)
        else:
            self.tanka = touyaku_kingaku_to_ten(kingaku)
        self.label = f"{drug.master.name} {drug.conduct_drug.amount: g}{drug.master.unit}"
        self.merge_key = "conduct-drug", sect, drug.master.iyakuhincode, drug.conduct_drug.amount


class KizaiSectionItemEx(SectionItemEx):
    def __init__(self, kizai: ConductKizaiFull):
        super().__init__()
        kingaku = kizai.master.kingaku * kizai.conduct_kizai.amount
        self.tanka = kizai_kingaku_to_ten(kingaku)
        self.label = f"{kizai.master.name} {kizai.conduct_kizai.amount}{kizai.master.unit}"
        self.merge_key = "kizai", kizai.master.kizaicode, kizai.conduct_kizai.amount


class RcptMeisai:
    def __init__(self):
        self.sect_map: Dict[MeisaiSectionComponent, List[SectionItemEx]] = {}
        for sect in consts.MeisaiSections:
            self.sect_map[sect] = []

    def add(self, sect: MeisaiSectionComponent, item: SectionItemEx):
        self.sect_map[sect].append(item)

    def get_sections(self) -> List[MeisaiSection]:
        return [
            MeisaiSection(
                name=sect.ident,
                label=sect.label,
                items=self.sect_map[sect],
                section_total_ten=sum(i.tanka * i.count for i in self.sect_map[sect])
            )
            for sect in consts.MeisaiSections
        ]


class RcptVisit:
    def __init__(self):
        self.meisai = RcptMeisai()

    def add_shinryou_list(self, shinryou_list: List[ShinryouFull], revision: houkatsu.Revision) -> None:
        houkatsu_map: Dict[str, HoukatsuKensaSectionEx] = {}
        for shinryou in shinryou_list:
            houkatsu_code = shinryou.master.houkatsukensa
            if houkatsu_code == consts.HoukatsuNone:
                master: ShinryouMaster = shinryou.master
                sect = shuukei_to_meisai_section(master.shuukeisaki)
                self.meisai.add(sect, SimpleShinryouSectionEx(master))
            else:
                hsect = houkatsu_map.get(houkatsu_code)
                if hsect is None:
                    hsect = HoukatsuKensaSectionEx(houkatsu_code, revision)
                    houkatsu_map[houkatsu_code] = hsect
                    self.meisai.add(consts.MeisaiSectionKensa, hsect)
                hsect.add(shinryou.master)
            for sect in houkatsu_map.values():
                sect.update()

    def add_drugs(self, drugs: List[DrugFull]) -> None:
        naifuku_map: Dict[Any, NaifukuSectionItemEx] = {}
        sect = consts.MeisaiSectionTouyaku
        for drug in drugs:
            cat: int = drug.drug.category
            if cat == consts.DrugCategoryNaifuku:
                ekey = naifuku_extend_key(drug.drug)
                ns = naifuku_map.get(ekey)
                if ns:
                    ns.add(drug)
                else:
                    ns = NaifukuSectionItemEx(drug)
                    naifuku_map[ekey] = ns
                    self.meisai.add(sect, ns)
            elif cat == consts.DrugCategoryTonpuku:
                self.meisai.add(sect, TonpukuSectionItemEx(drug))
            elif cat == consts.DrugCategoryGaiyou:
                self.meisai.add(sect, GaiyouSectionItemEx(drug))
        for ns in naifuku_map.values():
            ns.update()

    def add_conducts(self, conducts: List[ConductFull]) -> None:
        for conduct in conducts:
            sect = section_of_conduct(conduct.conduct)
            for shinryou in conduct.conduct_shinryou_list:
                self.meisai.add(sect, SimpleShinryouSectionEx(shinryou.master))
            for drug in conduct.conduct_drugs:
                self.meisai.add(sect, ConductDrugSectionItemEx(sect, drug))
            for kizai in conduct.conduct_kizai_list:
                self.meisai.add(sect, KizaiSectionItemEx(kizai))


def section_of_conduct(conduct: Conduct) -> consts.MeisaiSectionComponent:
    if conduct.kind == consts.ConductKindGazou:
        return consts.MeisaiSectionGazou
    else:
        return consts.MeisaiSectionShochi


def calc_rcpt_age_by_date(birthday: datetime.date, at: datetime.date) -> int:
    return calc_rcpt_age(birthday.year, birthday.month, birthday.day, at.year, at.month)


def calc_rcpt_age(bd_year, bd_month, bd_day, year, month) -> int:
    age = year - bd_year
    if month < bd_month:
        age -= 1
    elif month == bd_month:
        if bd_day > 1:
            age -= 1
    return age


def calc_shahokokuho_futan_wari(rcpt_age) -> int:
    if rcpt_age < 3:
        return 2
    elif rcpt_age >= 70:
        return 2
    else:
        return 3


def touyaku_kingaku_to_ten(kingaku) -> int:
    if kingaku <= 15.0:
        return 1
    else:
        return math.ceil((kingaku - 15.0) / 10.0) + 1


def shochi_kingaku_ten(kingaku) -> int:
    if kingaku <= 15.0:
        return 0
    else:
        return math.ceil((kingaku - 15.0) / 10.0) + 1


def round_half_up(value) -> int:
    return int(value + 0.5)


def kizai_kingaku_to_ten(kingaku) -> int:
    return round_half_up(kingaku / 10.0)


def shinryou_master_ten(master: ShinryouMaster) -> int:
    return int(float(master.tensuu))


shuukei_to_meisai_section_map = {
    consts.ShuukeiShoshin: consts.MeisaiSectionShoshinSaisin,
    consts.ShuukeiSaishinSaishin: consts.MeisaiSectionShoshinSaisin,
    consts.ShuukeiSaishinGairaiKanri: consts.MeisaiSectionShoshinSaisin,
    consts.ShuukeiSaishinJikangai: consts.MeisaiSectionShoshinSaisin,
    consts.ShuukeiSaishinKyuujitsu: consts.MeisaiSectionShoshinSaisin,
    consts.ShuukeiSaishinShinya: consts.MeisaiSectionShoshinSaisin,
    consts.ShuukeiShidou: consts.MeisaiSectionIgakuKanri,
    consts.ShuukeiZaitaku: consts.MeisaiSectionZaitaku,
    consts.ShuukeiKensa: consts.MeisaiSectionKensa,
    consts.ShuukeiGazouShindan: consts.MeisaiSectionGazou,
    consts.ShuukeiTouyakuNaifukuTonpukuChouzai: consts.MeisaiSectionTouyaku,
    consts.ShuukeiTouyakuGaiyouChouzai: consts.MeisaiSectionTouyaku,
    consts.ShuukeiTouyakuShohou: consts.MeisaiSectionTouyaku,
    consts.ShuukeiTouyakuMadoku: consts.MeisaiSectionTouyaku,
    consts.ShuukeiTouyakuChouki: consts.MeisaiSectionTouyaku,
    consts.ShuukeiChuushaSeibutsuEtc: consts.MeisaiSectionChuusha,
    consts.ShuukeiChuushaHika: consts.MeisaiSectionChuusha,
    consts.ShuukeiChuushaJoumyaku: consts.MeisaiSectionChuusha,
    consts.ShuukeiChuushaOthers: consts.MeisaiSectionChuusha,
    consts.ShuukeiShochi: consts.MeisaiSectionShochi,
    consts.ShuukeiShujutsuShujutsu: consts.MeisaiSectionSonota,
    consts.ShuukeiShujutsuYuketsu: consts.MeisaiSectionSonota,
    consts.ShuukeiMasui: consts.MeisaiSectionSonota,
    consts.ShuukeiOthers: consts.MeisaiSectionSonota
}


def shuukei_to_meisai_section(shuukei: str) -> consts.MeisaiSectionComponent:
    return shuukei_to_meisai_section_map.get(shuukei, consts.MeisaiSectionSonota)


def houkatsu_kensa_merge_key(houkatsu_code, shinryou_list: List[ShinryouFull]):
    shinryou_codes = sorted(s.master.shinryoucode for s in shinryou_list)
    return "houkatsu_kensa", houkatsu_code, shinryou_codes


def calc_kouhi_futan_wari(futansha: int) -> int:
    a = futansha // 1000000
    if a == 41:
        return 1
    b = futansha // 1000
    if b == 80136:
        return 1
    if b == 80137:
        return 0
    if b == 81136:
        return 1
    if b == 81137:
        return 0
    if a == 88:
        return 0
    print(f"Unknown kouhi futansha ({futansha}).", file=sys.stderr)
    return 0


def calc_futan_wari(hoken: Hoken, rcpt_age: int) -> int:
    futan_wari = 10
    if hoken.shahokokuho:
        futan_wari = calc_shahokokuho_futan_wari(rcpt_age)
        if hoken.shahokokuho.kourei > 0:
            futan_wari = hoken.shahokokuho.kourei
    if hoken.koukikourei:
        futan_wari = hoken.koukikourei.futan_wari
    if hoken.roujin:
        futan_wari = hoken.roujin.futan_wari
    for kouhi in [hoken.kouhi_1, hoken.kouhi_2, hoken.kouhi_3]:
        if kouhi:
            fw = calc_kouhi_futan_wari(kouhi.futansha)
            futan_wari = min(futan_wari, fw)
    return futan_wari


# 	public static int calcCharge(int ten, int futanWari){
# 		int c = ten * futanWari;
# 		int r = c % 10;
# 		if( r < 5 )
# 			c -= r;
# 		else
# 			c += (10 - r);
# 		return c;
# 	}

def calc_charge(ten: int, futan_wari: int) -> int:
    c = ten * futan_wari
    r = c % 10
    if r < 5:
        c -= r
    else:
        c += (10 - r)
    return c
