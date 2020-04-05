from collections import namedtuple


# wqueue_states

WqueueStateWaitExam = 0
WqueueStateInExam = 1
WqueueStateWaitCashier = 2
WqueueStateWaitDrug = 3
WqueueStateWaitReExam = 4
WqueueStateWaitAppoint = 5

# pharma_queue_states

PharmaQueueStateWaitPack = 0
PharmaQueueStateInPack = 1
PharmaQueueStatePackDone = 2

# disease_end_reasons

DiseaseEndReasonNotEnded = "N"
DiseaseEndReasonCured = "C"
DiseaseEndReasonStopped = "S"
DiseaseEndReasonDead = "D"

# drug_categories

DrugCategoryNaifuku = 0
DrugCategoryTonpuku = 1
DrugCategoryGaiyou = 2
DrugCategoryInjection = 3

# conduct_kinds

ConductKindHikaChuusha = 0
ConductKindJoumyakuChuusha = 1
ConductKindOtherChuusha = 2
ConductKindGazou = 3

# iyakuhin_zaikei

ZaikeiNaifuku = "1"
ZaikeiOther = "3"
ZaikeiChuusha = "4"
ZaikeiGaiyou = "6"
ZaikeiShikaYakuzai = "8"
ZaikeiShikaTokutei = "9"

# shuushokugo_info

SmallestPostfixShuushokugoCode = 8000
LargestPostfixShuushookugoCode = 8999

# meisai_sections


MeisaiSectionComponent = namedtuple("_MeisaiSectionComponent", "name ident label")


MeisaiSectionShoshinSaisin = MeisaiSectionComponent(
    "MeisaiSectionShoshinSaisin", "ShoshinSaisin", "初・再診料"
)
MeisaiSectionIgakuKanri = MeisaiSectionComponent(
    "MeisaiSectionIgakuKanri", "IgakuKanri", "医学管理等"
)
MeisaiSectionZaitaku = MeisaiSectionComponent("MeisaiSectionZaitaku", "Zaitaku", "在宅医療")
MeisaiSectionKensa = MeisaiSectionComponent("MeisaiSectionKensa", "Kensa", "検査")
MeisaiSectionGazou = MeisaiSectionComponent("MeisaiSectionGazou", "Gazou", "画像診断")
MeisaiSectionTouyaku = MeisaiSectionComponent("MeisaiSectionTouyaku", "Touyaku", "投薬")
MeisaiSectionChuusha = MeisaiSectionComponent("MeisaiSectionChuusha", "Chuusha", "注射")
MeisaiSectionShochi = MeisaiSectionComponent("MeisaiSectionShochi", "Shochi", "処置")
MeisaiSectionSonota = MeisaiSectionComponent("MeisaiSectionSonota", "Sonota", "その他")
MeisaiSections = [
    MeisaiSectionShoshinSaisin,
    MeisaiSectionIgakuKanri,
    MeisaiSectionZaitaku,
    MeisaiSectionKensa,
    MeisaiSectionGazou,
    MeisaiSectionTouyaku,
    MeisaiSectionChuusha,
    MeisaiSectionShochi,
    MeisaiSectionSonota,
]

# shuukeisaki

ShuukeiShoshin = "110"
ShuukeiSaishinSaishin = "120"
ShuukeiSaishinGairaiKanri = "122"
ShuukeiSaishinJikangai = "123"
ShuukeiSaishinKyuujitsu = "124"
ShuukeiSaishinShinya = "125"
ShuukeiShidou = "130"
ShuukeiZaitaku = "140"
ShuukeiTouyakuNaifukuTonpukuChouzai = "210"
ShuukeiTouyakuGaiyouChouzai = "230"
ShuukeiTouyakuShohou = "250"
ShuukeiTouyakuMadoku = "260"
ShuukeiTouyakuChouki = "270"
ShuukeiChuushaSeibutsuEtc = "300"
ShuukeiChuushaHika = "311"
ShuukeiChuushaJoumyaku = "321"
ShuukeiChuushaOthers = "331"
ShuukeiShochi = "400"
ShuukeiShujutsuShujutsu = "500"
ShuukeiShujutsuYuketsu = "502"
ShuukeiMasui = "540"
ShuukeiKensa = "600"
ShuukeiGazouShindan = "700"
ShuukeiOthers = "800"

# houkatsu_kensa

HoukatsuNone = "00"
HoukatsuKetsuekiKagaku = "01"
HoukatsuEndocrine = "02"
HoukatsuHepatitis = "03"
HoukatsuTumor = "04"
HoukatsuTumorMisc = "05"
HoukatsuCoagulo = "06"
HoukatsuAutoAntibody = "07"
HoukatsuTolerance = "08"
HoukatsuVirusTiter = "09"
HoukatsuVirusGlobulin = "10"
HoukatsuSpecificIgE = "11"
