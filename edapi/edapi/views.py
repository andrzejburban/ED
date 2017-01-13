""" Cornice services.
"""
from cornice import Service
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import *
import json
import re
import os
import commands
import subprocess
import ctypes
import ctypes.util

adres_baza='mysql+pymysql://root:409da0q@localhost/ed?charset=cp1250'

hello = Service(name='hello', path='/hello', description="Simplest app")

@hello.get()
def get_info(request):
    """Returns Hello in JSON."""
    return {'Hello': 'World'}

trace = Service(name='trace', path='/api/trace/{id}', description="trace app", cors_origins=('*',))

@trace.get()
def get_trace(request):
    key = request.matchdict['id']
    Base = declarative_base()
    class TRACE(Base):
        __tablename__ = 'trace2'
        ID=Column(Integer, primary_key=True)
        resultID=Column(Integer)
        x=Column(Integer)
        y=Column(Integer)

    db=create_engine(adres_baza,echo=True)
    Base.metadata.bind = db
    DBSession = sessionmaker(bind=db)
    session = DBSession()
    trace= session.query(TRACE).filter(TRACE.resultID==int(key)).all()
    payload={}
    mini=9999999999
    maxi=0
    print("TUTAJ")
    for i in trace:
        pom={}
        if(i.ID<mini): mini=i.ID
        if(i.ID>maxi): maxi=i.ID
        pom["ID"]=i.ID
        pom["resultID"]=i.resultID
        pom["x"]=i.x
        pom["y"]=i.y
        payload[str(pom["ID"])]=pom
    payload["mini"]=mini
    payload["maxi"]=maxi
    session.close()
    return payload

results = Service(name='results', path='/api/results/{id}', description="results app", cors_origins=('*',))

@results.get()
def get_result(request):
    rid = request.matchdict['id']
    Base = declarative_base()
    class RESULT(Base):
        __tablename__ = 'results'
        ID=Column(Integer, primary_key=True)
        pulse=Column(Integer)
        distance=Column(Integer)
        eof=Column(String(30,collation='cp1250_polish_ci'))
        eof_center=Column(Integer)

    db=create_engine(adres_baza,echo=True)
    Base.metadata.bind = db
    DBSession = sessionmaker(bind=db)
    session = DBSession()
    result = session.query(RESULT).filter(RESULT.ID==int(rid)).all()
    payload={}
    for i in result:
        pom={}
        pom["distance"]=i.distance
        pom["pulse"]=i.pulse
        pom["eof_center"]=i.eof_center
        payload[str(rid)]=pom
    session.close()
    return payload

@results.post()
def post_result(request):
    rid = request.matchdict['id']
    dane=json.loads(request.body)
    kom=dane["komentarz"]
    Base = declarative_base()
    class RESULT(Base):
        __tablename__ = 'results'
        ID=Column(Integer, primary_key=True)
        pulse=Column(Integer)
        distance=Column(Integer)
        eof=Column(String(30,collation='cp1250_polish_ci'))
        eof_center=Column(Integer)

    db=create_engine(adres_baza,echo=True)
    conn=db.connect()
    stmt=update(RESULT).where(RESULT.ID==int(rid)).values(descr=kom)
    conn.execute(stmt)
    conn.close()
    return {"status": "positive"}

@results.delete()
def delete_result(request):
    rid = request.matchdict['id']
    Base = declarative_base()
    class RESULT(Base):
        __tablename__ = 'results'
        ID=Column(Integer, primary_key=True)
        pulse=Column(Integer)
        distance=Column(Integer)
        eof=Column(String(30,collation='cp1250_polish_ci'))
        eof_center=Column(Integer)

    db=create_engine(adres_baza,echo=True)
    conn=db.connect()
    stmt=delete(RESULT).where(RESULT.ID==int(rid))
    conn.execute(stmt)
    conn.close()
    return {"status": "positive"}

wyniki = Service(name='wyniki', path='/api/wyniki/{id}/{port}/{dmin}/{dmax}', description="wyniki app", cors_origins=('*',))

@wyniki.get()
def get_wyniki(request):
    objid = request.matchdict['id']
    port = request.matchdict['port']
    dmin = request.matchdict['dmin']
    dmax = request.matchdict['dmax']
    Base = declarative_base()
    class WYNIKI(Base):
        __tablename__ = 'results'
        ID=Column(Integer, primary_key=True)
        pulse=Column(Integer)
        distance=Column(Integer)
        eof=Column(String(30,collation='cp1250_polish_ci'))
        eof_center=Column(Integer)

    db=create_engine(adres_baza, echo=True)
    Base.metadata.bind = db
    DBSession = sessionmaker(bind=db)
    session = DBSession()
    if(int(objid)==0 and int(port)==0 and str(dmin)=='0' and str(dmax)=='0'):
        wyniki=session.query(WYNIKI).filter(WYNIKI.pulse==int(20000)).order_by(WYNIKI.ID.desc()).all()
    licznik=0
    payload={}
    for i in wyniki:
        licznik+=1
        pom={}
        pom["ID"]=i.ID
        pom["pulse"]=i.pulse
        pom["distance"]=i.distance
        pom["eof_center"]=i.eof_center
        try:
            pom["eof"]=i.eof
        except AttributeError:
            pom["eof"]=None
        payload[str(licznik)]=pom
    payload["licznik"]=licznik
    session.close()
    return payload

