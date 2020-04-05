from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


Base = declarative_base()


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

    def to_dict(self):
        d = dict()
        d["patient_id"] = self.patient_id
        d["last_name"] = self.last_name
        d["first_name"] = self.first_name
        d["last_name_yomi"] = self.last_name_yomi
        d["first_name_yomi"] = self.first_name_yomi
        d["birthday"] = self.birthday
        d["sex"] = self.sex
        d["address"] = self.address
        d["phone"] = self.phone
        return d


class IyakuhinMaster(Base):
    __tablename__ = "iyakuhin_master_arch"
    iyakuhincode = Column("iyakuhincode", Integer, primary_key=True)
    name = Column("name", String)
    valid_from = Column("valid_from", Date, primary_key=True)
    valid_upto = Column("valid_upto", Date)


class VisitPatient:
    def __init__(self, visit, patient):
        self.visit = visit
        self.patient = patient


db_user = os.environ["MYCLINIC_DB_USER"]
db_pass = os.environ["MYCLINIC_DB_PASS"]
engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@localhost/myclinic?charset=utf8mb4&raw")
Session = sessionmaker(bind=engine)
session = Session()

