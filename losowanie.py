__author__ = 'andreas'
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
import numpy as np
import json
import random

adres_baza='mysql+pymysql://root:409da0q@localhost/ed?charset=cp1250'

def algorytm_test():
    eof=1
    Base = declarative_base()
    class TRACE(Base):
        __tablename__ = 'results'
        ID=Column(Integer, primary_key=True)
        pulse=Column(Integer)
        distance=Column(Integer)
        eof_center=Column(Integer)
        eof=Column(String(30))

    db=create_engine(adres_baza,echo=True)
    Base.metadata.bind = db
    DBSession = sessionmaker(bind=db)
    session = DBSession()
    trace= session.query(TRACE).all()
    numery_all=[]
    numery_wynik=[]
    for i in trace:
        numery_all.append(int(i.ID))
    session.close()
    for i in xrange(0,12):
        numer=random.choice(numery_all)
        numery_wynik.append(numer)
    print(numery_wynik)

algorytm_test()