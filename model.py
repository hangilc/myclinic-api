from sqlalchemy import Column, String, Integer, Float, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime
import re


Base = declarative_base()


def confirm_int(value):
    if not isinstance(value, int):
        raise Exception("int expected")
    return value


def confirm_str(value):
    if not isinstance(value, str):
        raise Exception("string expected")
    return value


def confirm_float(value):
    if not isinstance(value, float):
        raise Exception("float expected")
    return value


def cvt_to_date_string(src):
    if isinstance(src, datetime.date):
        return src.strftime("%Y-%m-%d")
    else:
        return src


def cvt_to_datetime_string(src):
    if isinstance(src, datetime.datetime):
        return src.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return src


_re_trailing_zero = re.compile(r"\.0*$")


def cvt_to_int(src):
    if isinstance(src, str):
        src = _re_trailing_zero.sub("", src)
    return int(src)


class BatchEnterByNamesRequest:
    def __init__(self, shinryou_names=None, conducts=None):
        self.shinryou_names = shinryou_names
        self.conducts = conducts
        

    def to_dict(self):
        d = dict()
        d["shinryouNames"] = [x for x in self.shinryou_names]
        d["conducts"] = [x.to_dict() for x in self.conducts]
        return d

    @staticmethod
    def from_dict(d):
        m = BatchEnterByNamesRequest()
        if "shinryouNames" in d:
            m.shinryou_names = [confirm_str(x) for x in d['shinryouNames']]
        if "conducts" in d:
            m.conducts = [EnterConductByNamesRequest.from_dict(x) for x in d['conducts']]
        return m

class BatchEnterRequest:
    def __init__(self, drugs=None, shinryou_list=None, conducts=None):
        self.drugs = drugs
        self.shinryou_list = shinryou_list
        self.conducts = conducts
        

    def to_dict(self):
        d = dict()
        d["drugs"] = [x.to_dict() for x in self.drugs]
        d["shinryouList"] = [x.to_dict() for x in self.shinryou_list]
        d["conducts"] = [x.to_dict() for x in self.conducts]
        return d

    @staticmethod
    def from_dict(d):
        m = BatchEnterRequest()
        if "drugs" in d:
            m.drugs = [DrugWithAttr.from_dict(x) for x in d['drugs']]
        if "shinryouList" in d:
            m.shinryou_list = [ShinryouWithAttr.from_dict(x) for x in d['shinryouList']]
        if "conducts" in d:
            m.conducts = [ConductEnterRequest.from_dict(x) for x in d['conducts']]
        return m

class BatchEnterResult:
    def __init__(self, shinryou_ids=None, conduct_ids=None):
        self.shinryou_ids = shinryou_ids
        self.conduct_ids = conduct_ids
        

    def to_dict(self):
        d = dict()
        d["shinryouIds"] = [cvt_to_int(x) for x in self.shinryou_ids]
        d["conductIds"] = [cvt_to_int(x) for x in self.conduct_ids]
        return d

    @staticmethod
    def from_dict(d):
        m = BatchEnterResult()
        if "shinryouIds" in d:
            m.shinryou_ids = [confirm_int(x) for x in d['shinryouIds']]
        if "conductIds" in d:
            m.conduct_ids = [confirm_int(x) for x in d['conductIds']]
        return m

class ByoumeiMaster(Base):
    __tablename__ = "shoubyoumei_master_arch"
    shoubyoumeicode = Column("shoubyoumeicode", Integer, primary_key=True)
    name = Column("name", String)
    valid_from = Column("valid_from", String, primary_key=True)
    valid_upto = Column("valid_upto", String)
    

    def __repr__(self):
        return "<ByoumeiMaster(shoubyoumeicode='%s', name='%s', valid_from='%s', valid_upto='%s')>" % (self.shoubyoumeicode, self.name, self.valid_from, self.valid_upto)

    def to_dict(self):
        d = dict()
        d["shoubyoumeicode"] = cvt_to_int(self.shoubyoumeicode)
        d["name"] = self.name
        d["validFrom"] = self.valid_from
        d["validUpto"] = self.valid_upto
        return d

    @staticmethod
    def from_dict(d):
        m = ByoumeiMaster()
        if "shoubyoumeicode" in d:
            m.shoubyoumeicode = confirm_int(d['shoubyoumeicode'])
        if "name" in d:
            m.name = confirm_str(d['name'])
        if "validFrom" in d:
            m.valid_from = confirm_str(d['validFrom'])
        if "validUpto" in d:
            m.valid_upto = confirm_str(d['validUpto'])
        return m

class Charge(Base):
    __tablename__ = "visit_charge"
    visit_id = Column("visit_id", Integer, primary_key=True)
    charge = Column("charge", Integer)
    

    def __repr__(self):
        return "<Charge(visit_id='%s', charge='%s')>" % (self.visit_id, self.charge)

    def to_dict(self):
        d = dict()
        d["visitId"] = cvt_to_int(self.visit_id)
        d["charge"] = cvt_to_int(self.charge)
        return d

    @staticmethod
    def from_dict(d):
        m = Charge()
        if "visitId" in d:
            m.visit_id = confirm_int(d['visitId'])
        if "charge" in d:
            m.charge = confirm_int(d['charge'])
        return m

class ChargeOptional:
    def __init__(self, charge=None):
        self.charge = charge
        

    def to_dict(self):
        d = dict()
        d["charge"] = self.charge.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = ChargeOptional()
        if "charge" in d:
            m.charge = Charge.from_dict(d['charge'])
        return m

class ClinicInfo:
    def __init__(self, name=None, postal_code=None, address=None, tel=None, fax=None, todoufukencode=None, tensuuhyoucode=None, kikancode=None, homepage=None, doctor_name=None):
        self.name = name
        self.postal_code = postal_code
        self.address = address
        self.tel = tel
        self.fax = fax
        self.todoufukencode = todoufukencode
        self.tensuuhyoucode = tensuuhyoucode
        self.kikancode = kikancode
        self.homepage = homepage
        self.doctor_name = doctor_name
        

    def to_dict(self):
        d = dict()
        d["name"] = self.name
        d["postalCode"] = self.postal_code
        d["address"] = self.address
        d["tel"] = self.tel
        d["fax"] = self.fax
        d["todoufukencode"] = self.todoufukencode
        d["tensuuhyoucode"] = self.tensuuhyoucode
        d["kikancode"] = self.kikancode
        d["homepage"] = self.homepage
        d["doctorName"] = self.doctor_name
        return d

    @staticmethod
    def from_dict(d):
        m = ClinicInfo()
        if "name" in d:
            m.name = confirm_str(d['name'])
        if "postalCode" in d:
            m.postal_code = confirm_str(d['postalCode'])
        if "address" in d:
            m.address = confirm_str(d['address'])
        if "tel" in d:
            m.tel = confirm_str(d['tel'])
        if "fax" in d:
            m.fax = confirm_str(d['fax'])
        if "todoufukencode" in d:
            m.todoufukencode = confirm_str(d['todoufukencode'])
        if "tensuuhyoucode" in d:
            m.tensuuhyoucode = confirm_str(d['tensuuhyoucode'])
        if "kikancode" in d:
            m.kikancode = confirm_str(d['kikancode'])
        if "homepage" in d:
            m.homepage = confirm_str(d['homepage'])
        if "doctorName" in d:
            m.doctor_name = confirm_str(d['doctorName'])
        return m

class ConductDrug(Base):
    __tablename__ = "visit_conduct_drug"
    conduct_drug_id = Column("id", Integer, primary_key=True)
    conduct_id = Column("visit_conduct_id", Integer)
    iyakuhincode = Column("iyakuhincode", Integer)
    amount = Column("amount", Float)
    

    def __repr__(self):
        return "<ConductDrug(conduct_drug_id='%s', conduct_id='%s', iyakuhincode='%s', amount='%s')>" % (self.conduct_drug_id, self.conduct_id, self.iyakuhincode, self.amount)

    def to_dict(self):
        d = dict()
        d["conductDrugId"] = None if self.conduct_drug_id is None else cvt_to_int(self.conduct_drug_id)
        d["conductId"] = cvt_to_int(self.conduct_id)
        d["iyakuhincode"] = cvt_to_int(self.iyakuhincode)
        d["amount"] = self.amount
        return d

    @staticmethod
    def from_dict(d):
        m = ConductDrug()
        if "conductDrugId" in d:
            m.conduct_drug_id = None if d['conductDrugId'] is None else confirm_int(d['conductDrugId'])
        if "conductId" in d:
            m.conduct_id = confirm_int(d['conductId'])
        if "iyakuhincode" in d:
            m.iyakuhincode = confirm_int(d['iyakuhincode'])
        if "amount" in d:
            m.amount = confirm_float(d['amount'])
        return m

class ConductDrugFull:
    def __init__(self, conduct_drug=None, master=None):
        self.conduct_drug = conduct_drug
        self.master = master
        

    def to_dict(self):
        d = dict()
        d["conductDrug"] = self.conduct_drug.to_dict()
        d["master"] = self.master.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = ConductDrugFull()
        if "conductDrug" in d:
            m.conduct_drug = ConductDrug.from_dict(d['conductDrug'])
        if "master" in d:
            m.master = IyakuhinMaster.from_dict(d['master'])
        return m

class Conduct(Base):
    __tablename__ = "visit_conduct"
    conduct_id = Column("id", Integer, primary_key=True)
    visit_id = Column("visit_id", Integer)
    kind = Column("kind", Integer)
    

    def __repr__(self):
        return "<Conduct(conduct_id='%s', visit_id='%s', kind='%s')>" % (self.conduct_id, self.visit_id, self.kind)

    def to_dict(self):
        d = dict()
        d["conductId"] = None if self.conduct_id is None else cvt_to_int(self.conduct_id)
        d["visitId"] = cvt_to_int(self.visit_id)
        d["kind"] = cvt_to_int(self.kind)
        return d

    @staticmethod
    def from_dict(d):
        m = Conduct()
        if "conductId" in d:
            m.conduct_id = None if d['conductId'] is None else confirm_int(d['conductId'])
        if "visitId" in d:
            m.visit_id = confirm_int(d['visitId'])
        if "kind" in d:
            m.kind = confirm_int(d['kind'])
        return m

class ConductEnterRequest:
    def __init__(self, visit_id=None, kind=None, gazou_label=None, shinryou_list=None, drugs=None, kizai_list=None):
        self.visit_id = visit_id
        self.kind = kind
        self.gazou_label = gazou_label
        self.shinryou_list = shinryou_list
        self.drugs = drugs
        self.kizai_list = kizai_list
        

    def to_dict(self):
        d = dict()
        d["visitId"] = cvt_to_int(self.visit_id)
        d["kind"] = cvt_to_int(self.kind)
        d["gazouLabel"] = self.gazou_label
        d["shinryouList"] = [x.to_dict() for x in self.shinryou_list]
        d["drugs"] = [x.to_dict() for x in self.drugs]
        d["kizaiList"] = [x.to_dict() for x in self.kizai_list]
        return d

    @staticmethod
    def from_dict(d):
        m = ConductEnterRequest()
        if "visitId" in d:
            m.visit_id = confirm_int(d['visitId'])
        if "kind" in d:
            m.kind = confirm_int(d['kind'])
        if "gazouLabel" in d:
            m.gazou_label = confirm_str(d['gazouLabel'])
        if "shinryouList" in d:
            m.shinryou_list = [ConductShinryou.from_dict(x) for x in d['shinryouList']]
        if "drugs" in d:
            m.drugs = [ConductDrug.from_dict(x) for x in d['drugs']]
        if "kizaiList" in d:
            m.kizai_list = [ConductKizai.from_dict(x) for x in d['kizaiList']]
        return m

class ConductFull:
    def __init__(self, conduct=None, gazou_label=None, conduct_shinryou_list=None, conduct_drugs=None, conduct_kizai_list=None):
        self.conduct = conduct
        self.gazou_label = gazou_label
        self.conduct_shinryou_list = conduct_shinryou_list
        self.conduct_drugs = conduct_drugs
        self.conduct_kizai_list = conduct_kizai_list
        

    def to_dict(self):
        d = dict()
        d["conduct"] = self.conduct.to_dict()
        d["gazouLabel"] = None if self.gazou_label is None else self.gazou_label.to_dict()
        d["conductShinryouList"] = [x.to_dict() for x in self.conduct_shinryou_list]
        d["conductDrugs"] = [x.to_dict() for x in self.conduct_drugs]
        d["conductKizaiList"] = [x.to_dict() for x in self.conduct_kizai_list]
        return d

    @staticmethod
    def from_dict(d):
        m = ConductFull()
        if "conduct" in d:
            m.conduct = Conduct.from_dict(d['conduct'])
        if "gazouLabel" in d:
            m.gazou_label = None if d['gazouLabel'] is None else GazouLabel.from_dict(d['gazouLabel'])
        if "conductShinryouList" in d:
            m.conduct_shinryou_list = [ConductShinryouFull.from_dict(x) for x in d['conductShinryouList']]
        if "conductDrugs" in d:
            m.conduct_drugs = [ConductDrugFull.from_dict(x) for x in d['conductDrugs']]
        if "conductKizaiList" in d:
            m.conduct_kizai_list = [ConductKizaiFull.from_dict(x) for x in d['conductKizaiList']]
        return m

class ConductKizai(Base):
    __tablename__ = "visit_conduct_kizai"
    conduct_kizai_id = Column("id", Integer, primary_key=True)
    conduct_id = Column("visit_conduct_id", Integer)
    kizaicode = Column("kizaicode", Integer)
    amount = Column("amount", Float)
    

    def __repr__(self):
        return "<ConductKizai(conduct_kizai_id='%s', conduct_id='%s', kizaicode='%s', amount='%s')>" % (self.conduct_kizai_id, self.conduct_id, self.kizaicode, self.amount)

    def to_dict(self):
        d = dict()
        d["conductKizaiId"] = None if self.conduct_kizai_id is None else cvt_to_int(self.conduct_kizai_id)
        d["conductId"] = cvt_to_int(self.conduct_id)
        d["kizaicode"] = cvt_to_int(self.kizaicode)
        d["amount"] = self.amount
        return d

    @staticmethod
    def from_dict(d):
        m = ConductKizai()
        if "conductKizaiId" in d:
            m.conduct_kizai_id = None if d['conductKizaiId'] is None else confirm_int(d['conductKizaiId'])
        if "conductId" in d:
            m.conduct_id = confirm_int(d['conductId'])
        if "kizaicode" in d:
            m.kizaicode = confirm_int(d['kizaicode'])
        if "amount" in d:
            m.amount = confirm_float(d['amount'])
        return m

class ConductKizaiFull:
    def __init__(self, conduct_kizai=None, master=None):
        self.conduct_kizai = conduct_kizai
        self.master = master
        

    def to_dict(self):
        d = dict()
        d["conductKizai"] = self.conduct_kizai.to_dict()
        d["master"] = self.master.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = ConductKizaiFull()
        if "conductKizai" in d:
            m.conduct_kizai = ConductKizai.from_dict(d['conductKizai'])
        if "master" in d:
            m.master = KizaiMaster.from_dict(d['master'])
        return m

class ConductShinryou(Base):
    __tablename__ = "visit_conduct_shinryou"
    conduct_shinryou_id = Column("id", Integer, primary_key=True)
    conduct_id = Column("visit_conduct_id", Integer)
    shinryoucode = Column("shinryoucode", Integer)
    

    def __repr__(self):
        return "<ConductShinryou(conduct_shinryou_id='%s', conduct_id='%s', shinryoucode='%s')>" % (self.conduct_shinryou_id, self.conduct_id, self.shinryoucode)

    def to_dict(self):
        d = dict()
        d["conductShinryouId"] = None if self.conduct_shinryou_id is None else cvt_to_int(self.conduct_shinryou_id)
        d["conductId"] = cvt_to_int(self.conduct_id)
        d["shinryoucode"] = cvt_to_int(self.shinryoucode)
        return d

    @staticmethod
    def from_dict(d):
        m = ConductShinryou()
        if "conductShinryouId" in d:
            m.conduct_shinryou_id = None if d['conductShinryouId'] is None else confirm_int(d['conductShinryouId'])
        if "conductId" in d:
            m.conduct_id = confirm_int(d['conductId'])
        if "shinryoucode" in d:
            m.shinryoucode = confirm_int(d['shinryoucode'])
        return m

class ConductShinryouFull:
    def __init__(self, conduct_shinryou=None, master=None):
        self.conduct_shinryou = conduct_shinryou
        self.master = master
        

    def to_dict(self):
        d = dict()
        d["conductShinryou"] = self.conduct_shinryou.to_dict()
        d["master"] = self.master.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = ConductShinryouFull()
        if "conductShinryou" in d:
            m.conduct_shinryou = ConductShinryou.from_dict(d['conductShinryou'])
        if "master" in d:
            m.master = ShinryouMaster.from_dict(d['master'])
        return m

class DiseaseAdj(Base):
    __tablename__ = "disease_adj"
    disease_adj_id = Column("disease_adj_id", Integer, primary_key=True)
    disease_id = Column("disease_id", Integer)
    shuushokugocode = Column("shuushokugocode", Integer)
    

    def __repr__(self):
        return "<DiseaseAdj(disease_adj_id='%s', disease_id='%s', shuushokugocode='%s')>" % (self.disease_adj_id, self.disease_id, self.shuushokugocode)

    def to_dict(self):
        d = dict()
        d["diseaseAdjId"] = None if self.disease_adj_id is None else cvt_to_int(self.disease_adj_id)
        d["diseaseId"] = cvt_to_int(self.disease_id)
        d["shuushokugocode"] = cvt_to_int(self.shuushokugocode)
        return d

    @staticmethod
    def from_dict(d):
        m = DiseaseAdj()
        if "diseaseAdjId" in d:
            m.disease_adj_id = None if d['diseaseAdjId'] is None else confirm_int(d['diseaseAdjId'])
        if "diseaseId" in d:
            m.disease_id = confirm_int(d['diseaseId'])
        if "shuushokugocode" in d:
            m.shuushokugocode = confirm_int(d['shuushokugocode'])
        return m

class DiseaseAdjFull:
    def __init__(self, disease_adj=None, master=None):
        self.disease_adj = disease_adj
        self.master = master
        

    def to_dict(self):
        d = dict()
        d["diseaseAdj"] = self.disease_adj.to_dict()
        d["master"] = self.master.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = DiseaseAdjFull()
        if "diseaseAdj" in d:
            m.disease_adj = DiseaseAdj.from_dict(d['diseaseAdj'])
        if "master" in d:
            m.master = ShuushokugoMaster.from_dict(d['master'])
        return m

class Disease(Base):
    __tablename__ = "disease"
    disease_id = Column("disease_id", Integer, primary_key=True)
    patient_id = Column("patient_id", Integer)
    shoubyoumeicode = Column("shoubyoumeicode", Integer)
    start_date = Column("start_date", Date)
    end_date = Column("end_date", Date)
    end_reason = Column("end_reason", String)
    

    def __repr__(self):
        return "<Disease(disease_id='%s', patient_id='%s', shoubyoumeicode='%s', start_date='%s', end_date='%s', end_reason='%s')>" % (self.disease_id, self.patient_id, self.shoubyoumeicode, self.start_date, self.end_date, self.end_reason)

    def to_dict(self):
        d = dict()
        d["diseaseId"] = None if self.disease_id is None else cvt_to_int(self.disease_id)
        d["patientId"] = cvt_to_int(self.patient_id)
        d["shoubyoumeicode"] = cvt_to_int(self.shoubyoumeicode)
        d["startDate"] = cvt_to_date_string(self.start_date)
        d["endDate"] = cvt_to_date_string(self.end_date)
        d["endReason"] = self.end_reason
        return d

    @staticmethod
    def from_dict(d):
        m = Disease()
        if "diseaseId" in d:
            m.disease_id = None if d['diseaseId'] is None else confirm_int(d['diseaseId'])
        if "patientId" in d:
            m.patient_id = confirm_int(d['patientId'])
        if "shoubyoumeicode" in d:
            m.shoubyoumeicode = confirm_int(d['shoubyoumeicode'])
        if "startDate" in d:
            m.start_date = confirm_str(d['startDate'])
        if "endDate" in d:
            m.end_date = confirm_str(d['endDate'])
        if "endReason" in d:
            m.end_reason = confirm_str(d['endReason'])
        return m

class DiseaseExample:
    def __init__(self, label=None, byoumei=None, adj_list=None):
        self.label = label
        self.byoumei = byoumei
        self.adj_list = adj_list
        

    def to_dict(self):
        d = dict()
        d["label"] = self.label
        d["byoumei"] = self.byoumei
        d["adjList"] = [x for x in self.adj_list]
        return d

    @staticmethod
    def from_dict(d):
        m = DiseaseExample()
        if "label" in d:
            m.label = confirm_str(d['label'])
        if "byoumei" in d:
            m.byoumei = confirm_str(d['byoumei'])
        if "adjList" in d:
            m.adj_list = [confirm_str(x) for x in d['adjList']]
        return m

class DiseaseFull:
    def __init__(self, disease=None, master=None, adj_list=None):
        self.disease = disease
        self.master = master
        self.adj_list = adj_list
        

    def to_dict(self):
        d = dict()
        d["disease"] = self.disease.to_dict()
        d["master"] = self.master.to_dict()
        d["adjList"] = [x.to_dict() for x in self.adj_list]
        return d

    @staticmethod
    def from_dict(d):
        m = DiseaseFull()
        if "disease" in d:
            m.disease = Disease.from_dict(d['disease'])
        if "master" in d:
            m.master = ByoumeiMaster.from_dict(d['master'])
        if "adjList" in d:
            m.adj_list = [DiseaseAdjFull.from_dict(x) for x in d['adjList']]
        return m

class DiseaseModify:
    def __init__(self, disease=None, shuushokugocodes=None):
        self.disease = disease
        self.shuushokugocodes = shuushokugocodes
        

    def to_dict(self):
        d = dict()
        d["disease"] = self.disease.to_dict()
        d["shuushokugocodes"] = [cvt_to_int(x) for x in self.shuushokugocodes]
        return d

    @staticmethod
    def from_dict(d):
        m = DiseaseModify()
        if "disease" in d:
            m.disease = Disease.from_dict(d['disease'])
        if "shuushokugocodes" in d:
            m.shuushokugocodes = [confirm_int(x) for x in d['shuushokugocodes']]
        return m

class DiseaseModifyEndReason:
    def __init__(self, disease_id=None, end_date=None, end_reason=None):
        self.disease_id = disease_id
        self.end_date = end_date
        self.end_reason = end_reason
        

    def to_dict(self):
        d = dict()
        d["diseaseId"] = cvt_to_int(self.disease_id)
        d["endDate"] = self.end_date
        d["endReason"] = self.end_reason
        return d

    @staticmethod
    def from_dict(d):
        m = DiseaseModifyEndReason()
        if "diseaseId" in d:
            m.disease_id = confirm_int(d['diseaseId'])
        if "endDate" in d:
            m.end_date = confirm_str(d['endDate'])
        if "endReason" in d:
            m.end_reason = confirm_str(d['endReason'])
        return m

class DiseaseNew:
    def __init__(self, disease=None, adj_list=None):
        self.disease = disease
        self.adj_list = adj_list
        

    def to_dict(self):
        d = dict()
        d["disease"] = self.disease.to_dict()
        d["adjList"] = [x.to_dict() for x in self.adj_list]
        return d

    @staticmethod
    def from_dict(d):
        m = DiseaseNew()
        if "disease" in d:
            m.disease = Disease.from_dict(d['disease'])
        if "adjList" in d:
            m.adj_list = [DiseaseAdj.from_dict(x) for x in d['adjList']]
        return m

class DrugAttr(Base):
    __tablename__ = "drug_attr"
    drug_id = Column("drug_id", Integer, primary_key=True)
    tekiyou = Column("tekiyou", String)
    

    def __repr__(self):
        return "<DrugAttr(drug_id='%s', tekiyou='%s')>" % (self.drug_id, self.tekiyou)

    def to_dict(self):
        d = dict()
        d["drugId"] = cvt_to_int(self.drug_id)
        d["tekiyou"] = self.tekiyou
        return d

    @staticmethod
    def from_dict(d):
        m = DrugAttr()
        if "drugId" in d:
            m.drug_id = confirm_int(d['drugId'])
        if "tekiyou" in d:
            m.tekiyou = confirm_str(d['tekiyou'])
        return m

class Drug(Base):
    __tablename__ = "visit_drug"
    drug_id = Column("drug_id", Integer, primary_key=True)
    visit_id = Column("visit_id", Integer)
    iyakuhincode = Column("d_iyakuhincode", Integer)
    amount = Column("d_amount", Float)
    usage = Column("d_usage", String)
    days = Column("d_days", Integer)
    category = Column("d_category", Integer)
    prescribed = Column("d_prescribed", Integer)
    

    def __repr__(self):
        return "<Drug(drug_id='%s', visit_id='%s', iyakuhincode='%s', amount='%s', usage='%s', days='%s', category='%s', prescribed='%s')>" % (self.drug_id, self.visit_id, self.iyakuhincode, self.amount, self.usage, self.days, self.category, self.prescribed)

    def to_dict(self):
        d = dict()
        d["drugId"] = None if self.drug_id is None else cvt_to_int(self.drug_id)
        d["visitId"] = cvt_to_int(self.visit_id)
        d["iyakuhincode"] = cvt_to_int(self.iyakuhincode)
        d["amount"] = self.amount
        d["usage"] = self.usage
        d["days"] = cvt_to_int(self.days)
        d["category"] = cvt_to_int(self.category)
        d["prescribed"] = cvt_to_int(self.prescribed)
        return d

    @staticmethod
    def from_dict(d):
        m = Drug()
        if "drugId" in d:
            m.drug_id = None if d['drugId'] is None else confirm_int(d['drugId'])
        if "visitId" in d:
            m.visit_id = confirm_int(d['visitId'])
        if "iyakuhincode" in d:
            m.iyakuhincode = confirm_int(d['iyakuhincode'])
        if "amount" in d:
            m.amount = confirm_float(d['amount'])
        if "usage" in d:
            m.usage = confirm_str(d['usage'])
        if "days" in d:
            m.days = confirm_int(d['days'])
        if "category" in d:
            m.category = confirm_int(d['category'])
        if "prescribed" in d:
            m.prescribed = confirm_int(d['prescribed'])
        return m

class DrugFull:
    def __init__(self, drug=None, master=None):
        self.drug = drug
        self.master = master
        

    def to_dict(self):
        d = dict()
        d["drug"] = self.drug.to_dict()
        d["master"] = self.master.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = DrugFull()
        if "drug" in d:
            m.drug = Drug.from_dict(d['drug'])
        if "master" in d:
            m.master = IyakuhinMaster.from_dict(d['master'])
        return m

class DrugFullWithAttr:
    def __init__(self, drug=None, attr=None):
        self.drug = drug
        self.attr = attr
        

    def to_dict(self):
        d = dict()
        d["drug"] = self.drug.to_dict()
        d["attr"] = self.attr.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = DrugFullWithAttr()
        if "drug" in d:
            m.drug = DrugFull.from_dict(d['drug'])
        if "attr" in d:
            m.attr = DrugAttr.from_dict(d['attr'])
        return m

class DrugWithAttr:
    def __init__(self, drug=None, attr=None):
        self.drug = drug
        self.attr = attr
        

    def to_dict(self):
        d = dict()
        d["drug"] = self.drug.to_dict()
        d["attr"] = self.attr.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = DrugWithAttr()
        if "drug" in d:
            m.drug = Drug.from_dict(d['drug'])
        if "attr" in d:
            m.attr = DrugAttr.from_dict(d['attr'])
        return m

class EnterConductByNamesRequest:
    def __init__(self, kind=None, gazou_label=None, shinryou_names=None, kizai_list=None):
        self.kind = kind
        self.gazou_label = gazou_label
        self.shinryou_names = shinryou_names
        self.kizai_list = kizai_list
        

    def to_dict(self):
        d = dict()
        d["kind"] = cvt_to_int(self.kind)
        d["gazouLabel"] = self.gazou_label
        d["shinryouNames"] = [x for x in self.shinryou_names]
        d["kizaiList"] = [x.to_dict() for x in self.kizai_list]
        return d

    @staticmethod
    def from_dict(d):
        m = EnterConductByNamesRequest()
        if "kind" in d:
            m.kind = confirm_int(d['kind'])
        if "gazouLabel" in d:
            m.gazou_label = confirm_str(d['gazouLabel'])
        if "shinryouNames" in d:
            m.shinryou_names = [confirm_str(x) for x in d['shinryouNames']]
        if "kizaiList" in d:
            m.kizai_list = [EnterConductKizaiByNamesRequest.from_dict(x) for x in d['kizaiList']]
        return m

class EnterConductKizaiByNamesRequest:
    def __init__(self, name=None, amount=None):
        self.name = name
        self.amount = amount
        

    def to_dict(self):
        d = dict()
        d["name"] = self.name
        d["amount"] = self.amount
        return d

    @staticmethod
    def from_dict(d):
        m = EnterConductKizaiByNamesRequest()
        if "name" in d:
            m.name = confirm_str(d['name'])
        if "amount" in d:
            m.amount = confirm_float(d['amount'])
        return m

class GazouLabel(Base):
    __tablename__ = "visit_gazou_label"
    conduct_id = Column("visit_conduct_id", Integer, primary_key=True)
    label = Column("label", String)
    

    def __repr__(self):
        return "<GazouLabel(conduct_id='%s', label='%s')>" % (self.conduct_id, self.label)

    def to_dict(self):
        d = dict()
        d["conductId"] = cvt_to_int(self.conduct_id)
        d["label"] = self.label
        return d

    @staticmethod
    def from_dict(d):
        m = GazouLabel()
        if "conductId" in d:
            m.conduct_id = confirm_int(d['conductId'])
        if "label" in d:
            m.label = confirm_str(d['label'])
        return m

class Hoken:
    def __init__(self, shahokokuho=None, koukikourei=None, roujin=None, kouhi_1=None, kouhi_2=None, kouhi_3=None):
        self.shahokokuho = shahokokuho
        self.koukikourei = koukikourei
        self.roujin = roujin
        self.kouhi_1 = kouhi_1
        self.kouhi_2 = kouhi_2
        self.kouhi_3 = kouhi_3
        

    def to_dict(self):
        d = dict()
        d["shahokokuho"] = None if self.shahokokuho is None else self.shahokokuho.to_dict()
        d["koukikourei"] = None if self.koukikourei is None else self.koukikourei.to_dict()
        d["roujin"] = None if self.roujin is None else self.roujin.to_dict()
        d["kouhi1"] = None if self.kouhi_1 is None else self.kouhi_1.to_dict()
        d["kouhi2"] = None if self.kouhi_2 is None else self.kouhi_2.to_dict()
        d["kouhi3"] = None if self.kouhi_3 is None else self.kouhi_3.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = Hoken()
        if "shahokokuho" in d:
            m.shahokokuho = None if d['shahokokuho'] is None else Shahokokuho.from_dict(d['shahokokuho'])
        if "koukikourei" in d:
            m.koukikourei = None if d['koukikourei'] is None else Koukikourei.from_dict(d['koukikourei'])
        if "roujin" in d:
            m.roujin = None if d['roujin'] is None else Roujin.from_dict(d['roujin'])
        if "kouhi1" in d:
            m.kouhi_1 = None if d['kouhi1'] is None else Kouhi.from_dict(d['kouhi1'])
        if "kouhi2" in d:
            m.kouhi_2 = None if d['kouhi2'] is None else Kouhi.from_dict(d['kouhi2'])
        if "kouhi3" in d:
            m.kouhi_3 = None if d['kouhi3'] is None else Kouhi.from_dict(d['kouhi3'])
        return m

class HokenList:
    def __init__(self, shahokokuho_list=None, koukikourei_list=None, roujin_list=None, kouhi_list=None):
        self.shahokokuho_list = shahokokuho_list
        self.koukikourei_list = koukikourei_list
        self.roujin_list = roujin_list
        self.kouhi_list = kouhi_list
        

    def to_dict(self):
        d = dict()
        d["shahokokuhoListDTO"] = [x.to_dict() for x in self.shahokokuho_list]
        d["koukikoureiListDTO"] = [x.to_dict() for x in self.koukikourei_list]
        d["roujinListDTO"] = [x.to_dict() for x in self.roujin_list]
        d["kouhiListDTO"] = [x.to_dict() for x in self.kouhi_list]
        return d

    @staticmethod
    def from_dict(d):
        m = HokenList()
        if "shahokokuhoListDTO" in d:
            m.shahokokuho_list = [Shahokokuho.from_dict(x) for x in d['shahokokuhoList']]
        if "koukikoureiListDTO" in d:
            m.koukikourei_list = [Koukikourei.from_dict(x) for x in d['koukikoureiList']]
        if "roujinListDTO" in d:
            m.roujin_list = [Roujin.from_dict(x) for x in d['roujinList']]
        if "kouhiListDTO" in d:
            m.kouhi_list = [Kouhi.from_dict(x) for x in d['kouhiList']]
        return m

class Hotline(Base):
    __tablename__ = "hotline"
    hotline_id = Column("hotline_id", Integer, primary_key=True)
    message = Column("message", String)
    sender = Column("sender", String)
    recipient = Column("recipient", String)
    posted_at = Column("m_datetime", DateTime)
    

    def __repr__(self):
        return "<Hotline(hotline_id='%s', message='%s', sender='%s', recipient='%s', posted_at='%s')>" % (self.hotline_id, self.message, self.sender, self.recipient, self.posted_at)

    def to_dict(self):
        d = dict()
        d["hotlineId"] = None if self.hotline_id is None else cvt_to_int(self.hotline_id)
        d["message"] = self.message
        d["sender"] = self.sender
        d["recipient"] = self.recipient
        d["postedAt"] = cvt_to_datetime_string(self.posted_at)
        return d

    @staticmethod
    def from_dict(d):
        m = Hotline()
        if "hotlineId" in d:
            m.hotline_id = None if d['hotlineId'] is None else confirm_int(d['hotlineId'])
        if "message" in d:
            m.message = confirm_str(d['message'])
        if "sender" in d:
            m.sender = confirm_str(d['sender'])
        if "recipient" in d:
            m.recipient = confirm_str(d['recipient'])
        if "postedAt" in d:
            m.posted_at = confirm_str(d['postedAt'])
        return m

class IntraclinicComment(Base):
    __tablename__ = "intraclinic_comment"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    content = Column("content", String)
    post_id = Column("post_id", Integer)
    created_at = Column("created_at", Date)
    

    def __repr__(self):
        return "<IntraclinicComment(id='%s', name='%s', content='%s', post_id='%s', created_at='%s')>" % (self.id, self.name, self.content, self.post_id, self.created_at)

    def to_dict(self):
        d = dict()
        d["id"] = None if self.id is None else cvt_to_int(self.id)
        d["name"] = self.name
        d["content"] = self.content
        d["postId"] = cvt_to_int(self.post_id)
        d["createdAt"] = cvt_to_date_string(self.created_at)
        return d

    @staticmethod
    def from_dict(d):
        m = IntraclinicComment()
        if "id" in d:
            m.id = None if d['id'] is None else confirm_int(d['id'])
        if "name" in d:
            m.name = confirm_str(d['name'])
        if "content" in d:
            m.content = confirm_str(d['content'])
        if "postId" in d:
            m.post_id = confirm_int(d['postId'])
        if "createdAt" in d:
            m.created_at = confirm_str(d['createdAt'])
        return m

class IntraclinicPost(Base):
    __tablename__ = "intraclinic_post"
    id = Column("id", Integer, primary_key=True)
    content = Column("content", String)
    created_at = Column("created_at", Date)
    

    def __repr__(self):
        return "<IntraclinicPost(id='%s', content='%s', created_at='%s')>" % (self.id, self.content, self.created_at)

    def to_dict(self):
        d = dict()
        d["id"] = None if self.id is None else cvt_to_int(self.id)
        d["content"] = self.content
        d["createdAt"] = cvt_to_date_string(self.created_at)
        return d

    @staticmethod
    def from_dict(d):
        m = IntraclinicPost()
        if "id" in d:
            m.id = None if d['id'] is None else confirm_int(d['id'])
        if "content" in d:
            m.content = confirm_str(d['content'])
        if "createdAt" in d:
            m.created_at = confirm_str(d['createdAt'])
        return m

class IntraclinicPostFull:
    def __init__(self, post=None, comments=None):
        self.post = post
        self.comments = comments
        

    def to_dict(self):
        d = dict()
        d["post"] = self.post.to_dict()
        d["comments"] = [x.to_dict() for x in self.comments]
        return d

    @staticmethod
    def from_dict(d):
        m = IntraclinicPostFull()
        if "post" in d:
            m.post = IntraclinicPost.from_dict(d['post'])
        if "comments" in d:
            m.comments = [IntraclinicComment.from_dict(x) for x in d['comments']]
        return m

class IntraclinicPostFullPage:
    def __init__(self, total_pages=None, posts=None):
        self.total_pages = total_pages
        self.posts = posts
        

    def to_dict(self):
        d = dict()
        d["totalPages"] = cvt_to_int(self.total_pages)
        d["posts"] = [x.to_dict() for x in self.posts]
        return d

    @staticmethod
    def from_dict(d):
        m = IntraclinicPostFullPage()
        if "totalPages" in d:
            m.total_pages = confirm_int(d['totalPages'])
        if "posts" in d:
            m.posts = [IntraclinicPostFull.from_dict(x) for x in d['posts']]
        return m

class IntraclinicPostPage:
    def __init__(self, total_pages=None, posts=None):
        self.total_pages = total_pages
        self.posts = posts
        

    def to_dict(self):
        d = dict()
        d["totalPages"] = cvt_to_int(self.total_pages)
        d["posts"] = [x.to_dict() for x in self.posts]
        return d

    @staticmethod
    def from_dict(d):
        m = IntraclinicPostPage()
        if "totalPages" in d:
            m.total_pages = confirm_int(d['totalPages'])
        if "posts" in d:
            m.posts = [IntraclinicPost.from_dict(x) for x in d['posts']]
        return m

class IntraclinicTag(Base):
    __tablename__ = "intraclinic_tag"
    tag_id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    

    def __repr__(self):
        return "<IntraclinicTag(tag_id='%s', name='%s')>" % (self.tag_id, self.name)

    def to_dict(self):
        d = dict()
        d["tagId"] = None if self.tag_id is None else cvt_to_int(self.tag_id)
        d["name"] = self.name
        return d

    @staticmethod
    def from_dict(d):
        m = IntraclinicTag()
        if "tagId" in d:
            m.tag_id = None if d['tagId'] is None else confirm_int(d['tagId'])
        if "name" in d:
            m.name = confirm_str(d['name'])
        return m

class IntraclinicTagPost:
    def __init__(self, tag_id=None, post_id=None):
        self.tag_id = tag_id
        self.post_id = post_id
        

    def to_dict(self):
        d = dict()
        d["tagId"] = cvt_to_int(self.tag_id)
        d["postId"] = cvt_to_int(self.post_id)
        return d

    @staticmethod
    def from_dict(d):
        m = IntraclinicTagPost()
        if "tagId" in d:
            m.tag_id = confirm_int(d['tagId'])
        if "postId" in d:
            m.post_id = confirm_int(d['postId'])
        return m

class IyakuhincodeName:
    def __init__(self, iyakuhincode=None, name=None):
        self.iyakuhincode = iyakuhincode
        self.name = name
        

    def to_dict(self):
        d = dict()
        d["iyakuhincode"] = cvt_to_int(self.iyakuhincode)
        d["name"] = self.name
        return d

    @staticmethod
    def from_dict(d):
        m = IyakuhincodeName()
        if "iyakuhincode" in d:
            m.iyakuhincode = confirm_int(d['iyakuhincode'])
        if "name" in d:
            m.name = confirm_str(d['name'])
        return m

class IyakuhinMaster(Base):
    __tablename__ = "iyakuhin_master_arch"
    iyakuhincode = Column("iyakuhincode", Integer, primary_key=True)
    valid_from = Column("valid_from", Date, primary_key=True)
    name = Column("name", String)
    yomi = Column("yomi", String)
    unit = Column("unit", String)
    yakka = Column("yakka", Float)
    madoku = Column("madoku", String)
    kouhatsu = Column("kouhatsu", String)
    zaikei = Column("zaikei", String)
    valid_upto = Column("valid_upto", Date)
    

    def __repr__(self):
        return "<IyakuhinMaster(iyakuhincode='%s', valid_from='%s', name='%s', yomi='%s', unit='%s', yakka='%s', madoku='%s', kouhatsu='%s', zaikei='%s', valid_upto='%s')>" % (self.iyakuhincode, self.valid_from, self.name, self.yomi, self.unit, self.yakka, self.madoku, self.kouhatsu, self.zaikei, self.valid_upto)

    def to_dict(self):
        d = dict()
        d["iyakuhincode"] = cvt_to_int(self.iyakuhincode)
        d["validFrom"] = cvt_to_date_string(self.valid_from)
        d["name"] = self.name
        d["yomi"] = self.yomi
        d["unit"] = self.unit
        d["yakka"] = self.yakka
        d["madoku"] = self.madoku
        d["kouhatsu"] = self.kouhatsu
        d["zaikei"] = self.zaikei
        d["validUpto"] = cvt_to_date_string(self.valid_upto)
        return d

    @staticmethod
    def from_dict(d):
        m = IyakuhinMaster()
        if "iyakuhincode" in d:
            m.iyakuhincode = confirm_int(d['iyakuhincode'])
        if "validFrom" in d:
            m.valid_from = confirm_str(d['validFrom'])
        if "name" in d:
            m.name = confirm_str(d['name'])
        if "yomi" in d:
            m.yomi = confirm_str(d['yomi'])
        if "unit" in d:
            m.unit = confirm_str(d['unit'])
        if "yakka" in d:
            m.yakka = confirm_float(d['yakka'])
        if "madoku" in d:
            m.madoku = confirm_str(d['madoku'])
        if "kouhatsu" in d:
            m.kouhatsu = confirm_str(d['kouhatsu'])
        if "zaikei" in d:
            m.zaikei = confirm_str(d['zaikei'])
        if "validUpto" in d:
            m.valid_upto = confirm_str(d['validUpto'])
        return m

class KizaiMaster(Base):
    __tablename__ = "tokuteikizai_master_arch"
    kizaicode = Column("kizaicode", Integer, primary_key=True)
    valid_from = Column("valid_from", Date, primary_key=True)
    name = Column("name", String)
    yomi = Column("yomi", String)
    unit = Column("unit", String)
    kingaku = Column("kingaku", Float)
    valid_upto = Column("valid_upto", Date)
    

    def __repr__(self):
        return "<KizaiMaster(kizaicode='%s', valid_from='%s', name='%s', yomi='%s', unit='%s', kingaku='%s', valid_upto='%s')>" % (self.kizaicode, self.valid_from, self.name, self.yomi, self.unit, self.kingaku, self.valid_upto)

    def to_dict(self):
        d = dict()
        d["kizaicode"] = cvt_to_int(self.kizaicode)
        d["validFrom"] = cvt_to_date_string(self.valid_from)
        d["name"] = self.name
        d["yomi"] = self.yomi
        d["unit"] = self.unit
        d["kingaku"] = self.kingaku
        d["validUpto"] = cvt_to_date_string(self.valid_upto)
        return d

    @staticmethod
    def from_dict(d):
        m = KizaiMaster()
        if "kizaicode" in d:
            m.kizaicode = confirm_int(d['kizaicode'])
        if "validFrom" in d:
            m.valid_from = confirm_str(d['validFrom'])
        if "name" in d:
            m.name = confirm_str(d['name'])
        if "yomi" in d:
            m.yomi = confirm_str(d['yomi'])
        if "unit" in d:
            m.unit = confirm_str(d['unit'])
        if "kingaku" in d:
            m.kingaku = confirm_float(d['kingaku'])
        if "validUpto" in d:
            m.valid_upto = confirm_str(d['validUpto'])
        return m

class Kouhi(Base):
    __tablename__ = "kouhi"
    kouhi_id = Column("kouhi_id", Integer, primary_key=True)
    patient_id = Column("patient_id", Integer)
    futansha = Column("futansha", Integer)
    jukyuusha = Column("jukyuusha", Integer)
    valid_from = Column("valid_from", Date)
    valid_upto = Column("valid_upto", Date)
    

    def __repr__(self):
        return "<Kouhi(kouhi_id='%s', patient_id='%s', futansha='%s', jukyuusha='%s', valid_from='%s', valid_upto='%s')>" % (self.kouhi_id, self.patient_id, self.futansha, self.jukyuusha, self.valid_from, self.valid_upto)

    def to_dict(self):
        d = dict()
        d["kouhiId"] = None if self.kouhi_id is None else cvt_to_int(self.kouhi_id)
        d["patientId"] = cvt_to_int(self.patient_id)
        d["futansha"] = cvt_to_int(self.futansha)
        d["jukyuusha"] = cvt_to_int(self.jukyuusha)
        d["validFrom"] = cvt_to_date_string(self.valid_from)
        d["validUpto"] = cvt_to_date_string(self.valid_upto)
        return d

    @staticmethod
    def from_dict(d):
        m = Kouhi()
        if "kouhiId" in d:
            m.kouhi_id = None if d['kouhiId'] is None else confirm_int(d['kouhiId'])
        if "patientId" in d:
            m.patient_id = confirm_int(d['patientId'])
        if "futansha" in d:
            m.futansha = confirm_int(d['futansha'])
        if "jukyuusha" in d:
            m.jukyuusha = confirm_int(d['jukyuusha'])
        if "validFrom" in d:
            m.valid_from = confirm_str(d['validFrom'])
        if "validUpto" in d:
            m.valid_upto = confirm_str(d['validUpto'])
        return m

class Koukikourei(Base):
    __tablename__ = "hoken_koukikourei"
    koukikourei_id = Column("koukikourei_id", Integer, primary_key=True)
    patient_id = Column("patient_id", Integer)
    hokensha_bangou = Column("hokensha_bangou", String)
    hihokensha_bangou = Column("hihokensha_bangou", String)
    futan_wari = Column("futan_wari", Integer)
    valid_from = Column("valid_from", Date)
    valid_upto = Column("valid_upto", Date)
    

    def __repr__(self):
        return "<Koukikourei(koukikourei_id='%s', patient_id='%s', hokensha_bangou='%s', hihokensha_bangou='%s', futan_wari='%s', valid_from='%s', valid_upto='%s')>" % (self.koukikourei_id, self.patient_id, self.hokensha_bangou, self.hihokensha_bangou, self.futan_wari, self.valid_from, self.valid_upto)

    def to_dict(self):
        d = dict()
        d["koukikoureiId"] = None if self.koukikourei_id is None else cvt_to_int(self.koukikourei_id)
        d["patientId"] = cvt_to_int(self.patient_id)
        d["hokenshaBangou"] = self.hokensha_bangou
        d["hihokenshaBangou"] = self.hihokensha_bangou
        d["futanWari"] = cvt_to_int(self.futan_wari)
        d["validFrom"] = cvt_to_date_string(self.valid_from)
        d["validUpto"] = cvt_to_date_string(self.valid_upto)
        return d

    @staticmethod
    def from_dict(d):
        m = Koukikourei()
        if "koukikoureiId" in d:
            m.koukikourei_id = None if d['koukikoureiId'] is None else confirm_int(d['koukikoureiId'])
        if "patientId" in d:
            m.patient_id = confirm_int(d['patientId'])
        if "hokenshaBangou" in d:
            m.hokensha_bangou = confirm_str(d['hokenshaBangou'])
        if "hihokenshaBangou" in d:
            m.hihokensha_bangou = confirm_str(d['hihokenshaBangou'])
        if "futanWari" in d:
            m.futan_wari = confirm_int(d['futanWari'])
        if "validFrom" in d:
            m.valid_from = confirm_str(d['validFrom'])
        if "validUpto" in d:
            m.valid_upto = confirm_str(d['validUpto'])
        return m

class Meisai:
    def __init__(self, sections=None, total_ten=None, futan_wari=None, charge=None, hoken=None):
        self.sections = sections
        self.total_ten = total_ten
        self.futan_wari = futan_wari
        self.charge = charge
        self.hoken = hoken
        

    def to_dict(self):
        d = dict()
        d["sections"] = [x.to_dict() for x in self.sections]
        d["totalTen"] = cvt_to_int(self.total_ten)
        d["futanWari"] = cvt_to_int(self.futan_wari)
        d["charge"] = cvt_to_int(self.charge)
        d["hoken"] = self.hoken.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = Meisai()
        if "sections" in d:
            m.sections = [MeisaiSection.from_dict(x) for x in d['sections']]
        if "totalTen" in d:
            m.total_ten = confirm_int(d['totalTen'])
        if "futanWari" in d:
            m.futan_wari = confirm_int(d['futanWari'])
        if "charge" in d:
            m.charge = confirm_int(d['charge'])
        if "hoken" in d:
            m.hoken = Hoken.from_dict(d['hoken'])
        return m

class MeisaiSection:
    def __init__(self, name=None, label=None, items=None, section_total_ten=None):
        self.name = name
        self.label = label
        self.items = items
        self.section_total_ten = section_total_ten
        

    def to_dict(self):
        d = dict()
        d["name"] = self.name
        d["label"] = self.label
        d["items"] = [x.to_dict() for x in self.items]
        d["sectionTotalTen"] = cvt_to_int(self.section_total_ten)
        return d

    @staticmethod
    def from_dict(d):
        m = MeisaiSection()
        if "name" in d:
            m.name = confirm_str(d['name'])
        if "label" in d:
            m.label = confirm_str(d['label'])
        if "items" in d:
            m.items = [SectionItem.from_dict(x) for x in d['items']]
        if "sectionTotalTen" in d:
            m.section_total_ten = confirm_int(d['sectionTotalTen'])
        return m

class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column("patient_id", Integer, primary_key=True)
    last_name = Column("last_name", String)
    first_name = Column("first_name", String)
    last_name_yomi = Column("last_name_yomi", String)
    first_name_yomi = Column("first_name_yomi", String)
    birthday = Column("birth_day", Date)
    sex = Column("sex", String)
    address = Column("address", String)
    phone = Column("phone", String)
    

    def __repr__(self):
        return "<Patient(patient_id='%s', last_name='%s', first_name='%s', last_name_yomi='%s', first_name_yomi='%s', birthday='%s', sex='%s', address='%s', phone='%s')>" % (self.patient_id, self.last_name, self.first_name, self.last_name_yomi, self.first_name_yomi, self.birthday, self.sex, self.address, self.phone)

    def to_dict(self):
        d = dict()
        d["patientId"] = None if self.patient_id is None else cvt_to_int(self.patient_id)
        d["lastName"] = self.last_name
        d["firstName"] = self.first_name
        d["lastNameYomi"] = self.last_name_yomi
        d["firstNameYomi"] = self.first_name_yomi
        d["birthday"] = cvt_to_date_string(self.birthday)
        d["sex"] = self.sex
        d["address"] = self.address
        d["phone"] = self.phone
        return d

    @staticmethod
    def from_dict(d):
        m = Patient()
        if "patientId" in d:
            m.patient_id = None if d['patientId'] is None else confirm_int(d['patientId'])
        if "lastName" in d:
            m.last_name = confirm_str(d['lastName'])
        if "firstName" in d:
            m.first_name = confirm_str(d['firstName'])
        if "lastNameYomi" in d:
            m.last_name_yomi = confirm_str(d['lastNameYomi'])
        if "firstNameYomi" in d:
            m.first_name_yomi = confirm_str(d['firstNameYomi'])
        if "birthday" in d:
            m.birthday = confirm_str(d['birthday'])
        if "sex" in d:
            m.sex = confirm_str(d['sex'])
        if "address" in d:
            m.address = confirm_str(d['address'])
        if "phone" in d:
            m.phone = confirm_str(d['phone'])
        return m

class PatientHoken:
    def __init__(self, patient=None, hoken=None):
        self.patient = patient
        self.hoken = hoken
        

    def to_dict(self):
        d = dict()
        d["patientDTO"] = self.patient.to_dict()
        d["hokenDTO"] = self.hoken.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = PatientHoken()
        if "patientDTO" in d:
            m.patient = Patient.from_dict(d['patient'])
        if "hokenDTO" in d:
            m.hoken = Hoken.from_dict(d['hoken'])
        return m

class PatientHokenList:
    def __init__(self, patient=None, hoken_list=None):
        self.patient = patient
        self.hoken_list = hoken_list
        

    def to_dict(self):
        d = dict()
        d["patientDTO"] = self.patient.to_dict()
        d["hokenListDTO"] = self.hoken_list.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = PatientHokenList()
        if "patientDTO" in d:
            m.patient = Patient.from_dict(d['patient'])
        if "hokenListDTO" in d:
            m.hoken_list = HokenList.from_dict(d['hokenList'])
        return m

class PatientIdTime:
    def __init__(self, patient_id=None, time=None):
        self.patient_id = patient_id
        self.time = time
        

    def to_dict(self):
        d = dict()
        d["patientId"] = cvt_to_int(self.patient_id)
        d["time"] = self.time
        return d

    @staticmethod
    def from_dict(d):
        m = PatientIdTime()
        if "patientId" in d:
            m.patient_id = confirm_int(d['patientId'])
        if "time" in d:
            m.time = confirm_str(d['time'])
        return m

class Payment(Base):
    __tablename__ = "visit_payment"
    visit_id = Column("visit_id", Integer, primary_key=True)
    amount = Column("amount", Integer)
    paytime = Column("paytime", DateTime, primary_key=True)
    

    def __repr__(self):
        return "<Payment(visit_id='%s', amount='%s', paytime='%s')>" % (self.visit_id, self.amount, self.paytime)

    def to_dict(self):
        d = dict()
        d["visitId"] = cvt_to_int(self.visit_id)
        d["amount"] = cvt_to_int(self.amount)
        d["paytime"] = cvt_to_datetime_string(self.paytime)
        return d

    @staticmethod
    def from_dict(d):
        m = Payment()
        if "visitId" in d:
            m.visit_id = confirm_int(d['visitId'])
        if "amount" in d:
            m.amount = confirm_int(d['amount'])
        if "paytime" in d:
            m.paytime = confirm_str(d['paytime'])
        return m

class PaymentVisitPatient:
    def __init__(self, payment=None, visit=None, patient=None):
        self.payment = payment
        self.visit = visit
        self.patient = patient
        

    def to_dict(self):
        d = dict()
        d["payment"] = self.payment.to_dict()
        d["visit"] = self.visit.to_dict()
        d["patient"] = self.patient.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = PaymentVisitPatient()
        if "payment" in d:
            m.payment = Payment.from_dict(d['payment'])
        if "visit" in d:
            m.visit = Visit.from_dict(d['visit'])
        if "patient" in d:
            m.patient = Patient.from_dict(d['patient'])
        return m

class PharmaDrug(Base):
    __tablename__ = "pharma_drug"
    iyakuhincode = Column("iyakuhincode", Integer, primary_key=True)
    description = Column("description", String)
    sideeffect = Column("sideeffect", String)
    

    def __repr__(self):
        return "<PharmaDrug(iyakuhincode='%s', description='%s', sideeffect='%s')>" % (self.iyakuhincode, self.description, self.sideeffect)

    def to_dict(self):
        d = dict()
        d["iyakuhincode"] = cvt_to_int(self.iyakuhincode)
        d["description"] = self.description
        d["sideeffect"] = self.sideeffect
        return d

    @staticmethod
    def from_dict(d):
        m = PharmaDrug()
        if "iyakuhincode" in d:
            m.iyakuhincode = confirm_int(d['iyakuhincode'])
        if "description" in d:
            m.description = confirm_str(d['description'])
        if "sideeffect" in d:
            m.sideeffect = confirm_str(d['sideeffect'])
        return m

class PharmaDrugName:
    def __init__(self, iyakuhincode=None, name=None, yomi=None):
        self.iyakuhincode = iyakuhincode
        self.name = name
        self.yomi = yomi
        

    def to_dict(self):
        d = dict()
        d["iyakuhincode"] = cvt_to_int(self.iyakuhincode)
        d["name"] = self.name
        d["yomi"] = self.yomi
        return d

    @staticmethod
    def from_dict(d):
        m = PharmaDrugName()
        if "iyakuhincode" in d:
            m.iyakuhincode = confirm_int(d['iyakuhincode'])
        if "name" in d:
            m.name = confirm_str(d['name'])
        if "yomi" in d:
            m.yomi = confirm_str(d['yomi'])
        return m

class PharmaQueue(Base):
    __tablename__ = "pharma_queue"
    visit_id = Column("visit_id", Integer, primary_key=True)
    pharma_state = Column("pharma_state", Integer)
    

    def __repr__(self):
        return "<PharmaQueue(visit_id='%s', pharma_state='%s')>" % (self.visit_id, self.pharma_state)

    def to_dict(self):
        d = dict()
        d["visitId"] = cvt_to_int(self.visit_id)
        d["pharmaState"] = cvt_to_int(self.pharma_state)
        return d

    @staticmethod
    def from_dict(d):
        m = PharmaQueue()
        if "visitId" in d:
            m.visit_id = confirm_int(d['visitId'])
        if "pharmaState" in d:
            m.pharma_state = confirm_int(d['pharmaState'])
        return m

class PharmaQueueFull:
    def __init__(self, visit_id=None, patient=None, pharma_queue=None, wqueue=None):
        self.visit_id = visit_id
        self.patient = patient
        self.pharma_queue = pharma_queue
        self.wqueue = wqueue
        

    def to_dict(self):
        d = dict()
        d["visitId"] = cvt_to_int(self.visit_id)
        d["patient"] = self.patient.to_dict()
        d["pharmaQueue"] = self.pharma_queue.to_dict()
        d["wqueue"] = self.wqueue.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = PharmaQueueFull()
        if "visitId" in d:
            m.visit_id = confirm_int(d['visitId'])
        if "patient" in d:
            m.patient = Patient.from_dict(d['patient'])
        if "pharmaQueue" in d:
            m.pharma_queue = PharmaQueue.from_dict(d['pharmaQueue'])
        if "wqueue" in d:
            m.wqueue = Wqueue.from_dict(d['wqueue'])
        return m

class PracticeConfig:
    def __init__(self, kouhatsu_kasan=None):
        self.kouhatsu_kasan = kouhatsu_kasan
        

    def to_dict(self):
        d = dict()
        d["kouhatsuKasan"] = self.kouhatsu_kasan
        return d

    @staticmethod
    def from_dict(d):
        m = PracticeConfig()
        if "kouhatsuKasan" in d:
            m.kouhatsu_kasan = confirm_str(d['kouhatsuKasan'])
        return m

class PracticeLog(Base):
    __tablename__ = "practice_log"
    serial_id = Column("practice_log_id", Integer, primary_key=True)
    created_at = Column("created_at", DateTime)
    kind = Column("kind", String)
    body = Column("body", String)
    

    def __repr__(self):
        return "<PracticeLog(serial_id='%s', created_at='%s', kind='%s', body='%s')>" % (self.serial_id, self.created_at, self.kind, self.body)

    def to_dict(self):
        d = dict()
        d["serialId"] = None if self.serial_id is None else cvt_to_int(self.serial_id)
        d["createdAt"] = cvt_to_datetime_string(self.created_at)
        d["kind"] = self.kind
        d["body"] = self.body
        return d

    @staticmethod
    def from_dict(d):
        m = PracticeLog()
        if "serialId" in d:
            m.serial_id = None if d['serialId'] is None else confirm_int(d['serialId'])
        if "createdAt" in d:
            m.created_at = confirm_str(d['createdAt'])
        if "kind" in d:
            m.kind = confirm_str(d['kind'])
        if "body" in d:
            m.body = confirm_str(d['body'])
        return m

class PrescExample(Base):
    __tablename__ = "presc_example"
    presc_example_id = Column("presc_example_id", Integer, primary_key=True)
    iyakuhincode = Column("m_iyakuhincode", Integer)
    master_valid_from = Column("m_master_valid_from", Date)
    amount = Column("m_amount", String)
    usage = Column("m_usage", String)
    days = Column("m_days", Integer)
    category = Column("m_category", Integer)
    comment = Column("m_comment", String)
    

    def __repr__(self):
        return "<PrescExample(presc_example_id='%s', iyakuhincode='%s', master_valid_from='%s', amount='%s', usage='%s', days='%s', category='%s', comment='%s')>" % (self.presc_example_id, self.iyakuhincode, self.master_valid_from, self.amount, self.usage, self.days, self.category, self.comment)

    def to_dict(self):
        d = dict()
        d["prescExampleId"] = None if self.presc_example_id is None else cvt_to_int(self.presc_example_id)
        d["iyakuhincode"] = cvt_to_int(self.iyakuhincode)
        d["masterValidFrom"] = cvt_to_date_string(self.master_valid_from)
        d["amount"] = self.amount
        d["usage"] = self.usage
        d["days"] = cvt_to_int(self.days)
        d["category"] = cvt_to_int(self.category)
        d["comment"] = self.comment
        return d

    @staticmethod
    def from_dict(d):
        m = PrescExample()
        if "prescExampleId" in d:
            m.presc_example_id = None if d['prescExampleId'] is None else confirm_int(d['prescExampleId'])
        if "iyakuhincode" in d:
            m.iyakuhincode = confirm_int(d['iyakuhincode'])
        if "masterValidFrom" in d:
            m.master_valid_from = confirm_str(d['masterValidFrom'])
        if "amount" in d:
            m.amount = confirm_str(d['amount'])
        if "usage" in d:
            m.usage = confirm_str(d['usage'])
        if "days" in d:
            m.days = confirm_int(d['days'])
        if "category" in d:
            m.category = confirm_int(d['category'])
        if "comment" in d:
            m.comment = confirm_str(d['comment'])
        return m

class PrescExampleFull:
    def __init__(self, presc_example=None, master=None):
        self.presc_example = presc_example
        self.master = master
        

    def to_dict(self):
        d = dict()
        d["prescExample"] = self.presc_example.to_dict()
        d["master"] = self.master.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = PrescExampleFull()
        if "prescExample" in d:
            m.presc_example = PrescExample.from_dict(d['prescExample'])
        if "master" in d:
            m.master = IyakuhinMaster.from_dict(d['master'])
        return m

class ReferItem:
    def __init__(self, hospital=None, section=None, doctor=None):
        self.hospital = hospital
        self.section = section
        self.doctor = doctor
        

    def to_dict(self):
        d = dict()
        d["hospital"] = self.hospital
        d["section"] = self.section
        d["doctor"] = self.doctor
        return d

    @staticmethod
    def from_dict(d):
        m = ReferItem()
        if "hospital" in d:
            m.hospital = confirm_str(d['hospital'])
        if "section" in d:
            m.section = confirm_str(d['section'])
        if "doctor" in d:
            m.doctor = confirm_str(d['doctor'])
        return m

class ResolvedStockDrug:
    def __init__(self, query_iyakuhincode=None, resolved_iyakuhincode=None):
        self.query_iyakuhincode = query_iyakuhincode
        self.resolved_iyakuhincode = resolved_iyakuhincode
        

    def to_dict(self):
        d = dict()
        d["queryIyakuhincode"] = cvt_to_int(self.query_iyakuhincode)
        d["resolvedIyakuhincode"] = cvt_to_int(self.resolved_iyakuhincode)
        return d

    @staticmethod
    def from_dict(d):
        m = ResolvedStockDrug()
        if "queryIyakuhincode" in d:
            m.query_iyakuhincode = confirm_int(d['queryIyakuhincode'])
        if "resolvedIyakuhincode" in d:
            m.resolved_iyakuhincode = confirm_int(d['resolvedIyakuhincode'])
        return m

class Roujin(Base):
    __tablename__ = "hoken_roujin"
    roujin_id = Column("roujin_id", Integer, primary_key=True)
    patient_id = Column("patient_id", Integer)
    shichouson = Column("shichouson", Integer)
    jukyuusha = Column("jukyuusha", Integer)
    futan_wari = Column("futan_wari", Integer)
    valid_from = Column("valid_from", Date)
    valid_upto = Column("valid_upto", Date)
    

    def __repr__(self):
        return "<Roujin(roujin_id='%s', patient_id='%s', shichouson='%s', jukyuusha='%s', futan_wari='%s', valid_from='%s', valid_upto='%s')>" % (self.roujin_id, self.patient_id, self.shichouson, self.jukyuusha, self.futan_wari, self.valid_from, self.valid_upto)

    def to_dict(self):
        d = dict()
        d["roujinId"] = None if self.roujin_id is None else cvt_to_int(self.roujin_id)
        d["patientId"] = cvt_to_int(self.patient_id)
        d["shichouson"] = cvt_to_int(self.shichouson)
        d["jukyuusha"] = cvt_to_int(self.jukyuusha)
        d["futanWari"] = cvt_to_int(self.futan_wari)
        d["validFrom"] = cvt_to_date_string(self.valid_from)
        d["validUpto"] = cvt_to_date_string(self.valid_upto)
        return d

    @staticmethod
    def from_dict(d):
        m = Roujin()
        if "roujinId" in d:
            m.roujin_id = None if d['roujinId'] is None else confirm_int(d['roujinId'])
        if "patientId" in d:
            m.patient_id = confirm_int(d['patientId'])
        if "shichouson" in d:
            m.shichouson = confirm_int(d['shichouson'])
        if "jukyuusha" in d:
            m.jukyuusha = confirm_int(d['jukyuusha'])
        if "futanWari" in d:
            m.futan_wari = confirm_int(d['futanWari'])
        if "validFrom" in d:
            m.valid_from = confirm_str(d['validFrom'])
        if "validUpto" in d:
            m.valid_upto = confirm_str(d['validUpto'])
        return m

class SectionItem:
    def __init__(self, label=None, tanka=None, count=None):
        self.label = label
        self.tanka = tanka
        self.count = count
        

    def to_dict(self):
        d = dict()
        d["label"] = self.label
        d["tanka"] = cvt_to_int(self.tanka)
        d["count"] = cvt_to_int(self.count)
        return d

    @staticmethod
    def from_dict(d):
        m = SectionItem()
        if "label" in d:
            m.label = confirm_str(d['label'])
        if "tanka" in d:
            m.tanka = confirm_int(d['tanka'])
        if "count" in d:
            m.count = confirm_int(d['count'])
        return m

class Shahokokuho(Base):
    __tablename__ = "hoken_shahokokuho"
    shahokokuho_id = Column("shahokokuho_id", Integer, primary_key=True)
    patient_id = Column("patient_id", Integer)
    hokensha_bangou = Column("hokensha_bangou", Integer)
    hihokensha_kigou = Column("hihokensha_kigou", String)
    hihokensha_bangou = Column("hihokensha_bangou", String)
    honnin = Column("honnin", Integer)
    kourei = Column("kourei", Integer)
    valid_from = Column("valid_from", Date)
    valid_upto = Column("valid_upto", Date)
    

    def __repr__(self):
        return "<Shahokokuho(shahokokuho_id='%s', patient_id='%s', hokensha_bangou='%s', hihokensha_kigou='%s', hihokensha_bangou='%s', honnin='%s', kourei='%s', valid_from='%s', valid_upto='%s')>" % (self.shahokokuho_id, self.patient_id, self.hokensha_bangou, self.hihokensha_kigou, self.hihokensha_bangou, self.honnin, self.kourei, self.valid_from, self.valid_upto)

    def to_dict(self):
        d = dict()
        d["shahokokuhoId"] = None if self.shahokokuho_id is None else cvt_to_int(self.shahokokuho_id)
        d["patientId"] = cvt_to_int(self.patient_id)
        d["hokenshaBangou"] = cvt_to_int(self.hokensha_bangou)
        d["hihokenshaKigou"] = self.hihokensha_kigou
        d["hihokenshaBangou"] = self.hihokensha_bangou
        d["honnin"] = cvt_to_int(self.honnin)
        d["kourei"] = cvt_to_int(self.kourei)
        d["validFrom"] = cvt_to_date_string(self.valid_from)
        d["validUpto"] = cvt_to_date_string(self.valid_upto)
        return d

    @staticmethod
    def from_dict(d):
        m = Shahokokuho()
        if "shahokokuhoId" in d:
            m.shahokokuho_id = None if d['shahokokuhoId'] is None else confirm_int(d['shahokokuhoId'])
        if "patientId" in d:
            m.patient_id = confirm_int(d['patientId'])
        if "hokenshaBangou" in d:
            m.hokensha_bangou = confirm_int(d['hokenshaBangou'])
        if "hihokenshaKigou" in d:
            m.hihokensha_kigou = confirm_str(d['hihokenshaKigou'])
        if "hihokenshaBangou" in d:
            m.hihokensha_bangou = confirm_str(d['hihokenshaBangou'])
        if "honnin" in d:
            m.honnin = confirm_int(d['honnin'])
        if "kourei" in d:
            m.kourei = confirm_int(d['kourei'])
        if "validFrom" in d:
            m.valid_from = confirm_str(d['validFrom'])
        if "validUpto" in d:
            m.valid_upto = confirm_str(d['validUpto'])
        return m

class ShinryouAttr(Base):
    __tablename__ = "shinryou_attr"
    shinryou_id = Column("shinryou_id", Integer, primary_key=True)
    tekiyou = Column("tekiyou", String)
    

    def __repr__(self):
        return "<ShinryouAttr(shinryou_id='%s', tekiyou='%s')>" % (self.shinryou_id, self.tekiyou)

    def to_dict(self):
        d = dict()
        d["shinryouId"] = cvt_to_int(self.shinryou_id)
        d["tekiyou"] = self.tekiyou
        return d

    @staticmethod
    def from_dict(d):
        m = ShinryouAttr()
        if "shinryouId" in d:
            m.shinryou_id = confirm_int(d['shinryouId'])
        if "tekiyou" in d:
            m.tekiyou = confirm_str(d['tekiyou'])
        return m

class Shinryou(Base):
    __tablename__ = "visit_shinryou"
    shinryou_id = Column("shinryou_id", Integer, primary_key=True)
    visit_id = Column("visit_id", Integer)
    shinryoucode = Column("shinryoucode", Integer)
    

    def __repr__(self):
        return "<Shinryou(shinryou_id='%s', visit_id='%s', shinryoucode='%s')>" % (self.shinryou_id, self.visit_id, self.shinryoucode)

    def to_dict(self):
        d = dict()
        d["shinryouId"] = None if self.shinryou_id is None else cvt_to_int(self.shinryou_id)
        d["visitId"] = cvt_to_int(self.visit_id)
        d["shinryoucode"] = cvt_to_int(self.shinryoucode)
        return d

    @staticmethod
    def from_dict(d):
        m = Shinryou()
        if "shinryouId" in d:
            m.shinryou_id = None if d['shinryouId'] is None else confirm_int(d['shinryouId'])
        if "visitId" in d:
            m.visit_id = confirm_int(d['visitId'])
        if "shinryoucode" in d:
            m.shinryoucode = confirm_int(d['shinryoucode'])
        return m

class ShinryouFull:
    def __init__(self, shinryou=None, master=None):
        self.shinryou = shinryou
        self.master = master
        

    def to_dict(self):
        d = dict()
        d["shinryou"] = self.shinryou.to_dict()
        d["master"] = self.master.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = ShinryouFull()
        if "shinryou" in d:
            m.shinryou = Shinryou.from_dict(d['shinryou'])
        if "master" in d:
            m.master = ShinryouMaster.from_dict(d['master'])
        return m

class ShinryouFullWithAttr:
    def __init__(self, shinryou=None, attr=None):
        self.shinryou = shinryou
        self.attr = attr
        

    def to_dict(self):
        d = dict()
        d["shinryou"] = self.shinryou.to_dict()
        d["attr"] = self.attr.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = ShinryouFullWithAttr()
        if "shinryou" in d:
            m.shinryou = ShinryouFull.from_dict(d['shinryou'])
        if "attr" in d:
            m.attr = ShinryouAttr.from_dict(d['attr'])
        return m

class ShinryouMaster(Base):
    __tablename__ = "shinryoukoui_master_arch"
    shinryoucode = Column("shinryoucode", Integer, primary_key=True)
    valid_from = Column("valid_from", Date, primary_key=True)
    name = Column("name", String)
    tensuu = Column("tensuu", Integer)
    tensuu_shikibetsu = Column("tensuu_shikibetsu", String)
    shuukeisaki = Column("shuukeisaki", String)
    houkatsukensa = Column("houkatsukensa", String)
    oushinkubun = Column("oushinkubun", String)
    kensa_group = Column("kensagroup", String)
    valid_upto = Column("valid_upto", Date)
    

    def __repr__(self):
        return "<ShinryouMaster(shinryoucode='%s', valid_from='%s', name='%s', tensuu='%s', tensuu_shikibetsu='%s', shuukeisaki='%s', houkatsukensa='%s', oushinkubun='%s', kensa_group='%s', valid_upto='%s')>" % (self.shinryoucode, self.valid_from, self.name, self.tensuu, self.tensuu_shikibetsu, self.shuukeisaki, self.houkatsukensa, self.oushinkubun, self.kensa_group, self.valid_upto)

    def to_dict(self):
        d = dict()
        d["shinryoucode"] = cvt_to_int(self.shinryoucode)
        d["validFrom"] = cvt_to_date_string(self.valid_from)
        d["name"] = self.name
        d["tensuu"] = cvt_to_int(self.tensuu)
        d["tensuuShikibetsu"] = self.tensuu_shikibetsu
        d["shuukeisaki"] = self.shuukeisaki
        d["houkatsukensa"] = self.houkatsukensa
        d["oushinkubun"] = self.oushinkubun
        d["kensaGroup"] = self.kensa_group
        d["validUpto"] = cvt_to_date_string(self.valid_upto)
        return d

    @staticmethod
    def from_dict(d):
        m = ShinryouMaster()
        if "shinryoucode" in d:
            m.shinryoucode = confirm_int(d['shinryoucode'])
        if "validFrom" in d:
            m.valid_from = confirm_str(d['validFrom'])
        if "name" in d:
            m.name = confirm_str(d['name'])
        if "tensuu" in d:
            m.tensuu = confirm_int(d['tensuu'])
        if "tensuuShikibetsu" in d:
            m.tensuu_shikibetsu = confirm_str(d['tensuuShikibetsu'])
        if "shuukeisaki" in d:
            m.shuukeisaki = confirm_str(d['shuukeisaki'])
        if "houkatsukensa" in d:
            m.houkatsukensa = confirm_str(d['houkatsukensa'])
        if "oushinkubun" in d:
            m.oushinkubun = confirm_str(d['oushinkubun'])
        if "kensaGroup" in d:
            m.kensa_group = confirm_str(d['kensaGroup'])
        if "validUpto" in d:
            m.valid_upto = confirm_str(d['validUpto'])
        return m

class ShinryouWithAttr:
    def __init__(self, shinryou=None, attr=None):
        self.shinryou = shinryou
        self.attr = attr
        

    def to_dict(self):
        d = dict()
        d["shinryou"] = self.shinryou.to_dict()
        d["attr"] = self.attr.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = ShinryouWithAttr()
        if "shinryou" in d:
            m.shinryou = Shinryou.from_dict(d['shinryou'])
        if "attr" in d:
            m.attr = ShinryouAttr.from_dict(d['attr'])
        return m

class Shouki(Base):
    __tablename__ = "shouki"
    visit_id = Column("visit_id", Integer, primary_key=True)
    shouki = Column("shouki", String)
    

    def __repr__(self):
        return "<Shouki(visit_id='%s', shouki='%s')>" % (self.visit_id, self.shouki)

    def to_dict(self):
        d = dict()
        d["visitId"] = cvt_to_int(self.visit_id)
        d["shouki"] = self.shouki
        return d

    @staticmethod
    def from_dict(d):
        m = Shouki()
        if "visitId" in d:
            m.visit_id = confirm_int(d['visitId'])
        if "shouki" in d:
            m.shouki = confirm_str(d['shouki'])
        return m

class ShuushokugoMaster(Base):
    __tablename__ = "shuushokugo_master"
    shuushokugocode = Column("shuushokugocode", Integer, primary_key=True)
    name = Column("name", String)
    

    def __repr__(self):
        return "<ShuushokugoMaster(shuushokugocode='%s', name='%s')>" % (self.shuushokugocode, self.name)

    def to_dict(self):
        d = dict()
        d["shuushokugocode"] = cvt_to_int(self.shuushokugocode)
        d["name"] = self.name
        return d

    @staticmethod
    def from_dict(d):
        m = ShuushokugoMaster()
        if "shuushokugocode" in d:
            m.shuushokugocode = confirm_int(d['shuushokugocode'])
        if "name" in d:
            m.name = confirm_str(d['name'])
        return m

class StringResult:
    def __init__(self, value=None):
        self.value = value
        

    def to_dict(self):
        d = dict()
        d["value"] = self.value
        return d

    @staticmethod
    def from_dict(d):
        m = StringResult()
        if "value" in d:
            m.value = confirm_str(d['value'])
        return m

class Text(Base):
    __tablename__ = "visit_text"
    text_id = Column("text_id", Integer, primary_key=True)
    visit_id = Column("visit_id", Integer)
    content = Column("content", String)
    

    def __repr__(self):
        return "<Text(text_id='%s', visit_id='%s', content='%s')>" % (self.text_id, self.visit_id, self.content)

    def to_dict(self):
        d = dict()
        d["textId"] = None if self.text_id is None else cvt_to_int(self.text_id)
        d["visitId"] = cvt_to_int(self.visit_id)
        d["content"] = self.content
        return d

    @staticmethod
    def from_dict(d):
        m = Text()
        if "textId" in d:
            m.text_id = None if d['textId'] is None else confirm_int(d['textId'])
        if "visitId" in d:
            m.visit_id = confirm_int(d['visitId'])
        if "content" in d:
            m.content = confirm_str(d['content'])
        return m

class TextVisit:
    def __init__(self, text=None, visit=None):
        self.text = text
        self.visit = visit
        

    def to_dict(self):
        d = dict()
        d["text"] = self.text.to_dict()
        d["visit"] = self.visit.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = TextVisit()
        if "text" in d:
            m.text = Text.from_dict(d['text'])
        if "visit" in d:
            m.visit = Visit.from_dict(d['visit'])
        return m

class TextVisitPage:
    def __init__(self, total_pages=None, page=None, text_visits=None):
        self.total_pages = total_pages
        self.page = page
        self.text_visits = text_visits
        

    def to_dict(self):
        d = dict()
        d["totalPages"] = cvt_to_int(self.total_pages)
        d["page"] = cvt_to_int(self.page)
        d["textVisits"] = [x.to_dict() for x in self.text_visits]
        return d

    @staticmethod
    def from_dict(d):
        m = TextVisitPage()
        if "totalPages" in d:
            m.total_pages = confirm_int(d['totalPages'])
        if "page" in d:
            m.page = confirm_int(d['page'])
        if "textVisits" in d:
            m.text_visits = [TextVisit.from_dict(x) for x in d['textVisits']]
        return m

class TextVisitPatient:
    def __init__(self, text=None, visit=None, patient=None):
        self.text = text
        self.visit = visit
        self.patient = patient
        

    def to_dict(self):
        d = dict()
        d["text"] = self.text.to_dict()
        d["visit"] = self.visit.to_dict()
        d["patient"] = self.patient.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = TextVisitPatient()
        if "text" in d:
            m.text = Text.from_dict(d['text'])
        if "visit" in d:
            m.visit = Visit.from_dict(d['visit'])
        if "patient" in d:
            m.patient = Patient.from_dict(d['patient'])
        return m

class TextVisitPatientPage:
    def __init__(self, total_pages=None, page=None, text_visit_patients=None):
        self.total_pages = total_pages
        self.page = page
        self.text_visit_patients = text_visit_patients
        

    def to_dict(self):
        d = dict()
        d["totalPages"] = cvt_to_int(self.total_pages)
        d["page"] = cvt_to_int(self.page)
        d["textVisitPatients"] = [x.to_dict() for x in self.text_visit_patients]
        return d

    @staticmethod
    def from_dict(d):
        m = TextVisitPatientPage()
        if "totalPages" in d:
            m.total_pages = confirm_int(d['totalPages'])
        if "page" in d:
            m.page = confirm_int(d['page'])
        if "textVisitPatients" in d:
            m.text_visit_patients = [TextVisitPatient.from_dict(x) for x in d['textVisitPatients']]
        return m

class TodaysVisitsWithLogInfo:
    def __init__(self, server_id=None, serial_id=None, visits=None):
        self.server_id = server_id
        self.serial_id = serial_id
        self.visits = visits
        

    def to_dict(self):
        d = dict()
        d["serverId"] = self.server_id
        d["serialId"] = cvt_to_int(self.serial_id)
        d["visits"] = [x.to_dict() for x in self.visits]
        return d

    @staticmethod
    def from_dict(d):
        m = TodaysVisitsWithLogInfo()
        if "serverId" in d:
            m.server_id = confirm_str(d['serverId'])
        if "serialId" in d:
            m.serial_id = confirm_int(d['serialId'])
        if "visits" in d:
            m.visits = [VisitFull2Patient.from_dict(x) for x in d['visits']]
        return m

class UpdateHoken:
    def __init__(self, visit_id=None, shahokokuho_id=None, koukikourei_id=None, roujin_id=None, kouhi_1_id=None, kouhi_2_id=None, kouhi_3_id=None):
        self.visit_id = visit_id
        self.shahokokuho_id = shahokokuho_id
        self.koukikourei_id = koukikourei_id
        self.roujin_id = roujin_id
        self.kouhi_1_id = kouhi_1_id
        self.kouhi_2_id = kouhi_2_id
        self.kouhi_3_id = kouhi_3_id
        

    def to_dict(self):
        d = dict()
        d["visitId"] = cvt_to_int(self.visit_id)
        d["shahokokuhoId"] = None if self.shahokokuho_id is None else cvt_to_int(self.shahokokuho_id)
        d["koukikoureiId"] = None if self.koukikourei_id is None else cvt_to_int(self.koukikourei_id)
        d["roujinId"] = None if self.roujin_id is None else cvt_to_int(self.roujin_id)
        d["kouhi1Id"] = None if self.kouhi_1_id is None else cvt_to_int(self.kouhi_1_id)
        d["kouhi2Id"] = None if self.kouhi_2_id is None else cvt_to_int(self.kouhi_2_id)
        d["kouhi3Id"] = None if self.kouhi_3_id is None else cvt_to_int(self.kouhi_3_id)
        return d

    @staticmethod
    def from_dict(d):
        m = UpdateHoken()
        if "visitId" in d:
            m.visit_id = confirm_int(d['visitId'])
        if "shahokokuhoId" in d:
            m.shahokokuho_id = None if d['shahokokuhoId'] is None else confirm_int(d['shahokokuhoId'])
        if "koukikoureiId" in d:
            m.koukikourei_id = None if d['koukikoureiId'] is None else confirm_int(d['koukikoureiId'])
        if "roujinId" in d:
            m.roujin_id = None if d['roujinId'] is None else confirm_int(d['roujinId'])
        if "kouhi1Id" in d:
            m.kouhi_1_id = None if d['kouhi1Id'] is None else confirm_int(d['kouhi1Id'])
        if "kouhi2Id" in d:
            m.kouhi_2_id = None if d['kouhi2Id'] is None else confirm_int(d['kouhi2Id'])
        if "kouhi3Id" in d:
            m.kouhi_3_id = None if d['kouhi3Id'] is None else confirm_int(d['kouhi3Id'])
        return m

class UserInfo:
    def __init__(self, user=None, name=None, roles=None):
        self.user = user
        self.name = name
        self.roles = roles
        

    def to_dict(self):
        d = dict()
        d["user"] = self.user
        d["name"] = self.name
        d["roles"] = [x for x in self.roles]
        return d

    @staticmethod
    def from_dict(d):
        m = UserInfo()
        if "user" in d:
            m.user = confirm_str(d['user'])
        if "name" in d:
            m.name = confirm_str(d['name'])
        if "roles" in d:
            m.roles = [confirm_str(x) for x in d['roles']]
        return m

class VisitChargePatient:
    def __init__(self, visit=None, charge=None, patient=None):
        self.visit = visit
        self.charge = charge
        self.patient = patient
        

    def to_dict(self):
        d = dict()
        d["visit"] = self.visit.to_dict()
        d["charge"] = self.charge.to_dict()
        d["patient"] = self.patient.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = VisitChargePatient()
        if "visit" in d:
            m.visit = Visit.from_dict(d['visit'])
        if "charge" in d:
            m.charge = Charge.from_dict(d['charge'])
        if "patient" in d:
            m.patient = Patient.from_dict(d['patient'])
        return m

class VisitDrug:
    def __init__(self, visit=None, drugs=None):
        self.visit = visit
        self.drugs = drugs
        

    def to_dict(self):
        d = dict()
        d["visit"] = self.visit.to_dict()
        d["drugs"] = [x.to_dict() for x in self.drugs]
        return d

    @staticmethod
    def from_dict(d):
        m = VisitDrug()
        if "visit" in d:
            m.visit = Visit.from_dict(d['visit'])
        if "drugs" in d:
            m.drugs = [DrugFull.from_dict(x) for x in d['drugs']]
        return m

class VisitDrugPage:
    def __init__(self, page=None, total_pages=None, visit_drugs=None):
        self.page = page
        self.total_pages = total_pages
        self.visit_drugs = visit_drugs
        

    def to_dict(self):
        d = dict()
        d["page"] = cvt_to_int(self.page)
        d["totalPages"] = cvt_to_int(self.total_pages)
        d["visitDrugs"] = [x.to_dict() for x in self.visit_drugs]
        return d

    @staticmethod
    def from_dict(d):
        m = VisitDrugPage()
        if "page" in d:
            m.page = confirm_int(d['page'])
        if "totalPages" in d:
            m.total_pages = confirm_int(d['totalPages'])
        if "visitDrugs" in d:
            m.visit_drugs = [VisitDrug.from_dict(x) for x in d['visitDrugs']]
        return m

class Visit(Base):
    __tablename__ = "visit"
    visit_id = Column("visit_id", Integer, primary_key=True)
    patient_id = Column("patient_id", Integer)
    visited_at = Column("v_datetime", DateTime)
    shahokokuho_id = Column("shahokokuho_id", Integer)
    koukikourei_id = Column("koukikourei_id", Integer)
    roujin_id = Column("roujin_id", Integer)
    kouhi_1_id = Column("kouhi_1_id", Integer)
    kouhi_2_id = Column("kouhi_2_id", Integer)
    kouhi_3_id = Column("kouhi_3_id", Integer)
    

    def __repr__(self):
        return "<Visit(visit_id='%s', patient_id='%s', visited_at='%s', shahokokuho_id='%s', koukikourei_id='%s', roujin_id='%s', kouhi_1_id='%s', kouhi_2_id='%s', kouhi_3_id='%s')>" % (self.visit_id, self.patient_id, self.visited_at, self.shahokokuho_id, self.koukikourei_id, self.roujin_id, self.kouhi_1_id, self.kouhi_2_id, self.kouhi_3_id)

    def to_dict(self):
        d = dict()
        d["visitId"] = None if self.visit_id is None else cvt_to_int(self.visit_id)
        d["patientId"] = cvt_to_int(self.patient_id)
        d["visitedAt"] = cvt_to_datetime_string(self.visited_at)
        d["shahokokuhoId"] = cvt_to_int(self.shahokokuho_id)
        d["koukikoureiId"] = cvt_to_int(self.koukikourei_id)
        d["roujinId"] = cvt_to_int(self.roujin_id)
        d["kouhi1Id"] = cvt_to_int(self.kouhi_1_id)
        d["kouhi2Id"] = cvt_to_int(self.kouhi_2_id)
        d["kouhi3Id"] = cvt_to_int(self.kouhi_3_id)
        return d

    @staticmethod
    def from_dict(d):
        m = Visit()
        if "visitId" in d:
            m.visit_id = None if d['visitId'] is None else confirm_int(d['visitId'])
        if "patientId" in d:
            m.patient_id = confirm_int(d['patientId'])
        if "visitedAt" in d:
            m.visited_at = confirm_str(d['visitedAt'])
        if "shahokokuhoId" in d:
            m.shahokokuho_id = confirm_int(d['shahokokuhoId'])
        if "koukikoureiId" in d:
            m.koukikourei_id = confirm_int(d['koukikoureiId'])
        if "roujinId" in d:
            m.roujin_id = confirm_int(d['roujinId'])
        if "kouhi1Id" in d:
            m.kouhi_1_id = confirm_int(d['kouhi1Id'])
        if "kouhi2Id" in d:
            m.kouhi_2_id = confirm_int(d['kouhi2Id'])
        if "kouhi3Id" in d:
            m.kouhi_3_id = confirm_int(d['kouhi3Id'])
        return m

class VisitFull2:
    def __init__(self, visit=None, texts=None, shinryou_list=None, drugs=None, conducts=None, hoken=None, charge=None):
        self.visit = visit
        self.texts = texts
        self.shinryou_list = shinryou_list
        self.drugs = drugs
        self.conducts = conducts
        self.hoken = hoken
        self.charge = charge
        

    def to_dict(self):
        d = dict()
        d["visit"] = self.visit.to_dict()
        d["texts"] = [x.to_dict() for x in self.texts]
        d["shinryouList"] = [x.to_dict() for x in self.shinryou_list]
        d["drugs"] = [x.to_dict() for x in self.drugs]
        d["conducts"] = [x.to_dict() for x in self.conducts]
        d["hoken"] = self.hoken.to_dict()
        d["charge"] = None if self.charge is None else self.charge.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = VisitFull2()
        if "visit" in d:
            m.visit = Visit.from_dict(d['visit'])
        if "texts" in d:
            m.texts = [Text.from_dict(x) for x in d['texts']]
        if "shinryouList" in d:
            m.shinryou_list = [ShinryouFull.from_dict(x) for x in d['shinryouList']]
        if "drugs" in d:
            m.drugs = [DrugFull.from_dict(x) for x in d['drugs']]
        if "conducts" in d:
            m.conducts = [ConductFull.from_dict(x) for x in d['conducts']]
        if "hoken" in d:
            m.hoken = Hoken.from_dict(d['hoken'])
        if "charge" in d:
            m.charge = None if d['charge'] is None else Charge.from_dict(d['charge'])
        return m

class VisitFull2Page:
    def __init__(self, total_pages=None, page=None, visits=None):
        self.total_pages = total_pages
        self.page = page
        self.visits = visits
        

    def to_dict(self):
        d = dict()
        d["totalPages"] = cvt_to_int(self.total_pages)
        d["page"] = cvt_to_int(self.page)
        d["visits"] = [x.to_dict() for x in self.visits]
        return d

    @staticmethod
    def from_dict(d):
        m = VisitFull2Page()
        if "totalPages" in d:
            m.total_pages = confirm_int(d['totalPages'])
        if "page" in d:
            m.page = confirm_int(d['page'])
        if "visits" in d:
            m.visits = [VisitFull2.from_dict(x) for x in d['visits']]
        return m

class VisitFull2Patient:
    def __init__(self, visit_full=None, patient=None):
        self.visit_full = visit_full
        self.patient = patient
        

    def to_dict(self):
        d = dict()
        d["visitFull"] = self.visit_full.to_dict()
        d["patient"] = self.patient.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = VisitFull2Patient()
        if "visitFull" in d:
            m.visit_full = VisitFull2.from_dict(d['visitFull'])
        if "patient" in d:
            m.patient = Patient.from_dict(d['patient'])
        return m

class VisitFull2PatientPage:
    def __init__(self, total_pages=None, page=None, visit_patients=None):
        self.total_pages = total_pages
        self.page = page
        self.visit_patients = visit_patients
        

    def to_dict(self):
        d = dict()
        d["totalPages"] = cvt_to_int(self.total_pages)
        d["page"] = cvt_to_int(self.page)
        d["visitPatients"] = [x.to_dict() for x in self.visit_patients]
        return d

    @staticmethod
    def from_dict(d):
        m = VisitFull2PatientPage()
        if "totalPages" in d:
            m.total_pages = confirm_int(d['totalPages'])
        if "page" in d:
            m.page = confirm_int(d['page'])
        if "visitPatients" in d:
            m.visit_patients = [VisitFull2Patient.from_dict(x) for x in d['visitPatients']]
        return m

class VisitFull:
    def __init__(self, visit=None, texts=None, shinryou_list=None, drugs=None, conducts=None):
        self.visit = visit
        self.texts = texts
        self.shinryou_list = shinryou_list
        self.drugs = drugs
        self.conducts = conducts
        

    def to_dict(self):
        d = dict()
        d["visit"] = self.visit.to_dict()
        d["texts"] = [x.to_dict() for x in self.texts]
        d["shinryouList"] = [x.to_dict() for x in self.shinryou_list]
        d["drugs"] = [x.to_dict() for x in self.drugs]
        d["conducts"] = [x.to_dict() for x in self.conducts]
        return d

    @staticmethod
    def from_dict(d):
        m = VisitFull()
        if "visit" in d:
            m.visit = Visit.from_dict(d['visit'])
        if "texts" in d:
            m.texts = [Text.from_dict(x) for x in d['texts']]
        if "shinryouList" in d:
            m.shinryou_list = [ShinryouFull.from_dict(x) for x in d['shinryouList']]
        if "drugs" in d:
            m.drugs = [DrugFull.from_dict(x) for x in d['drugs']]
        if "conducts" in d:
            m.conducts = [ConductFull.from_dict(x) for x in d['conducts']]
        return m

class VisitFullPage:
    def __init__(self, total_pages=None, page=None, visits=None):
        self.total_pages = total_pages
        self.page = page
        self.visits = visits
        

    def to_dict(self):
        d = dict()
        d["totalPages"] = cvt_to_int(self.total_pages)
        d["page"] = cvt_to_int(self.page)
        d["visits"] = [x.to_dict() for x in self.visits]
        return d

    @staticmethod
    def from_dict(d):
        m = VisitFullPage()
        if "totalPages" in d:
            m.total_pages = confirm_int(d['totalPages'])
        if "page" in d:
            m.page = confirm_int(d['page'])
        if "visits" in d:
            m.visits = [VisitFull.from_dict(x) for x in d['visits']]
        return m

class VisitIdVisitedAt:
    def __init__(self, visit_id=None, visited_at=None):
        self.visit_id = visit_id
        self.visited_at = visited_at
        

    def to_dict(self):
        d = dict()
        d["visitId"] = cvt_to_int(self.visit_id)
        d["visitedAt"] = self.visited_at
        return d

    @staticmethod
    def from_dict(d):
        m = VisitIdVisitedAt()
        if "visitId" in d:
            m.visit_id = confirm_int(d['visitId'])
        if "visitedAt" in d:
            m.visited_at = confirm_str(d['visitedAt'])
        return m

class VisitPatient:
    def __init__(self, visit=None, patient=None):
        self.visit = visit
        self.patient = patient
        

    def to_dict(self):
        d = dict()
        d["visit"] = self.visit.to_dict()
        d["patient"] = self.patient.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = VisitPatient()
        if "visit" in d:
            m.visit = Visit.from_dict(d['visit'])
        if "patient" in d:
            m.patient = Patient.from_dict(d['patient'])
        return m

class VisitTextDrug:
    def __init__(self, visit=None, texts=None, drugs=None):
        self.visit = visit
        self.texts = texts
        self.drugs = drugs
        

    def to_dict(self):
        d = dict()
        d["visit"] = self.visit.to_dict()
        d["texts"] = [x.to_dict() for x in self.texts]
        d["drugs"] = [x.to_dict() for x in self.drugs]
        return d

    @staticmethod
    def from_dict(d):
        m = VisitTextDrug()
        if "visit" in d:
            m.visit = Visit.from_dict(d['visit'])
        if "texts" in d:
            m.texts = [Text.from_dict(x) for x in d['texts']]
        if "drugs" in d:
            m.drugs = [DrugFull.from_dict(x) for x in d['drugs']]
        return m

class VisitTextDrugPage:
    def __init__(self, total_pages=None, page=None, visit_text_drugs=None):
        self.total_pages = total_pages
        self.page = page
        self.visit_text_drugs = visit_text_drugs
        

    def to_dict(self):
        d = dict()
        d["totalPages"] = cvt_to_int(self.total_pages)
        d["page"] = cvt_to_int(self.page)
        d["visitTextDrugs"] = [x.to_dict() for x in self.visit_text_drugs]
        return d

    @staticmethod
    def from_dict(d):
        m = VisitTextDrugPage()
        if "totalPages" in d:
            m.total_pages = confirm_int(d['totalPages'])
        if "page" in d:
            m.page = confirm_int(d['page'])
        if "visitTextDrugs" in d:
            m.visit_text_drugs = [VisitTextDrug.from_dict(x) for x in d['visitTextDrugs']]
        return m

class Wqueue(Base):
    __tablename__ = "wqueue"
    visit_id = Column("visit_id", Integer, primary_key=True)
    wait_state = Column("wait_state", Integer)
    

    def __repr__(self):
        return "<Wqueue(visit_id='%s', wait_state='%s')>" % (self.visit_id, self.wait_state)

    def to_dict(self):
        d = dict()
        d["visitId"] = cvt_to_int(self.visit_id)
        d["waitState"] = cvt_to_int(self.wait_state)
        return d

    @staticmethod
    def from_dict(d):
        m = Wqueue()
        if "visitId" in d:
            m.visit_id = confirm_int(d['visitId'])
        if "waitState" in d:
            m.wait_state = confirm_int(d['waitState'])
        return m

class WqueueFull:
    def __init__(self, wqueue=None, visit=None, patient=None):
        self.wqueue = wqueue
        self.visit = visit
        self.patient = patient
        

    def to_dict(self):
        d = dict()
        d["wqueue"] = self.wqueue.to_dict()
        d["visit"] = self.visit.to_dict()
        d["patient"] = self.patient.to_dict()
        return d

    @staticmethod
    def from_dict(d):
        m = WqueueFull()
        if "wqueue" in d:
            m.wqueue = Wqueue.from_dict(d['wqueue'])
        if "visit" in d:
            m.visit = Visit.from_dict(d['visit'])
        if "patient" in d:
            m.patient = Patient.from_dict(d['patient'])
        return m

