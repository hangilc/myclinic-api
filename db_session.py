import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


db_user = os.environ["MYCLINIC_DB_USER"]
db_pass = os.environ["MYCLINIC_DB_PASS"]
engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@localhost/myclinic?charset=utf8&raw", echo=False)
Session = sessionmaker(bind=engine)
