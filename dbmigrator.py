__author__ = 'andreas'
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import *
import json
import re
import os
import commands
import subprocess
import time

adres_baza_src='mysql+pymysql://root:409da0q@localhost/fms?charset=cp1250'
adres_baza_dst='mysql+pymysql://root:409da0q@localhost/ed?charset=cp1250'

def migrate_trace(trid):
    Base = declarative_base()
    Base2 = declarative_base()
    class TRACE_SRC(Base):
        __tablename__ = 'trace'
        ID=Column(Integer, primary_key=True)
        resultID=Column(Integer)
        x=Column(Integer)
        y=Column(Integer)

    class TRACE_DST(Base2):
        __tablename__ = 'trace'
        ID=Column(Integer, primary_key=True)
        resultID=Column(Integer)
        x=Column(Integer)
        y=Column(Integer)

    class RESULT_SRC(Base):
        __tablename__ = 'results'
        ID=Column(Integer, primary_key=True)
        pulse=Column(Integer)
        distance=Column(Integer)
        eof=Column(String(30,collation='cp1250_polish_ci'))
        eof_center=Column(Integer)

    class RESULT_DST(Base2):
        __tablename__ = 'results'
        ID=Column(Integer, primary_key=True)
        pulse=Column(Integer)
        distance=Column(Integer)
        eof=Column(String(30,collation='cp1250_general_ci'))
        eof_center=Column(Integer)

    db_dst=create_engine(adres_baza_dst,echo=True)
    conn=db_dst.connect()
    db_src=create_engine(adres_baza_src,echo=True)
    Base.metadata.bind = db_src
    DBSession = sessionmaker(bind=db_src)
    session = DBSession()
    Base2.metadata.bind = db_dst
    DBSession2 = sessionmaker(bind=db_dst)
    session2 = DBSession2()
    trace_src= session.query(TRACE_SRC).filter(TRACE_SRC.resultID==int(trid)).order_by(TRACE_SRC.ID).all()
    for_max=session2.query(RESULT_DST).all()
    maks=0
    for i in for_max:
        if(int(i.ID)>maks):
            maks=int(i.ID)
    payload={}
    mini=9999999999
    maxi=0
    for i in trace_src:
        pom={}
        if(i.ID<mini): mini=i.ID
        if(i.ID>maxi): maxi=i.ID
        pom["ID"]=i.ID
        pom["resultID"]=i.resultID
        pom["x"]=i.x
        pom["y"]=i.y
        payload[str(pom["ID"])]=pom
    results_src=session.query(RESULT_SRC).filter(RESULT_SRC.ID==int(trid)).all()
    for x in results_src:
        payload["resID"]=x.ID
        payload["respulse"]=x.pulse
        payload["resdistance"]=x.distance
        payload["reseof"]=x.eof
        payload["reseof_center"]=x.eof_center

    #tutaj musze napisac kod do zapisu do funkcji docelowej
    stmt2=insert(RESULT_DST).values(ID=maks+1,pulse=payload["respulse"],distance=payload["resdistance"],eof=payload["reseof"],eof_center=payload["reseof_center"])
    conn.execute(stmt2)
    for i in range(mini,maxi):
        objects=[]
        if(payload[str(i)] is not 'null'):
            #stmt=insert(TRACE_DST).values(resultID=maks+1,x=payload[str(i)]["x"],y=payload[str(i)]["y"])
            #conn.execute(stmt)
            #objects.append(TRACE_DST(resultID=maks+1,x=payload[str(i)]["x"],y=payload[str(i)]["y"]))
            session2.add(TRACE_DST(resultID=maks+1,x=payload[str(i)]["x"],y=payload[str(i)]["y"]))
    #session2.add_all(objects)
    session2.commit()
    session.close()
    session2.close()

def migrate_db():
    Base3 = declarative_base()
    class RESULT_SRC(Base3):
        __tablename__ = 'results'
        ID=Column(Integer, primary_key=True)
        pulse=Column(Integer)
        distance=Column(Integer)
        eof=Column(String(30,collation='cp1250_polish_ci'))
        eof_center=Column(Integer)
    db_src=create_engine(adres_baza_src,echo=True)
    Base3.metadata.bind = db_src
    DBSession3 = sessionmaker(bind=db_src)
    session3 = DBSession3()
    IDs=[]
    results= session3.query(RESULT_SRC).all()
    for i in results:
        IDs.append(i.ID)
    IDs=list(set(IDs))
    IDs.sort()
    for i in IDs:
        migrate_trace(int(i))

migrate_db()
