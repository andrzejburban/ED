__author__ = 'andreas'
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
import matplotlib.pyplot as plt
import numpy as np
import json
import re

adres_baza='mysql+pymysql://root:409da0q@localhost/ed?charset=cp1250'

def algorytm_test(key):
    eof=1
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
    trace= session.query(TRACE).filter(TRACE.resultID==int(key)).order_by(TRACE.x).all()
    payload={}
    mini=9999999999
    maxi=0
    x_axis=[]
    y_axis=[]
    for i in trace:
        pom={}
        if(i.ID<mini): mini=i.ID
        if(i.ID>maxi): maxi=i.ID
        x_axis.append(i.x)
        y_axis.append(i.y)
    session.close()
    jump=10
    new_y_axis=y_axis
    noise_avg=9000
    for i in xrange(0,len(y_axis)):
        if(x_axis[i]>=104000):
            noise_avg=np.mean(y_axis[i:len(y_axis)])-200
            print("NOISE_AVG: ",noise_avg)
            break
    for i in range(0,len(y_axis),1):
        if(y_axis[i]>=12000):
            y_axis[i]=12000
        elif(y_axis[i]<=noise_avg):#ten if jest opcjonalny i jeszcze nie do konca ustalony co do wartosci
            pass#y_axis[i]=noise_avg
    for i in range(0,len(y_axis),jump):
        if(i+jump<len(y_axis)):
            avg=np.var(y_axis[i:i+jump])
            for j in range(i,i+jump):
                y_axis[j]=avg
        else:
            avg=np.var(y_axis[i:len(y_axis)])
            for j in range(i,len(y_axis)):
                y_axis[j]=avg
    new_y_axis=np.unique(y_axis)
    srednia=np.mean(new_y_axis)
    mediana=np.median(new_y_axis)
    for i in range(0,len(y_axis),1):
        if(y_axis[i]>=srednia):
            y_axis[i]=mediana
    new_y_axis=np.unique(y_axis)
    current_max=np.max(y_axis)
    for i in range(0,len(y_axis)):
        if(y_axis[i]>=0.27*current_max):
            eof=x_axis[i]-3200
            break
    if(eof<4000):
        eof=4000
    #plt.plot(x_axis,y_axis)
    #plt.show()
    return eof

eof=algorytm_test(4228)
print("Koniec lini w: ",eof)
