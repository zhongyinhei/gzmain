# -*- coding: utf-8 -*-
from sqlalchemy import create_engine, Column, Integer, String,LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SURL = "mysql+pymysql://cic_admin:TaBoq,,1234@192.168.1.170:3306/yct_proxy?charset=utf8&autocommit=true"
engine = create_engine(SURL)  # 定义引擎
Base = declarative_base()
session = sessionmaker(engine)()


class YCTGZIP(Base):
    __tablename__ = 'yctjdugip'
    id = Column(Integer, primary_key=True)
    token = Column(String(50))
    ip = Column(String(50))
    state = Column(String(20))


class YCTCATLOG(Base):
    __tablename__ = 'yctcatlog'
    id = Column(Integer, primary_key=True)
    license = Column(String(20))
    chapter = Column(String(20))
    matter = Column(String(20))
    bespoke = Column(String(20))
    company_name = Column(String(50))
    yctAppNo = Column(String(50))
    # pagecode = Column(LargeBinary)
    lincense_state = Column(String(10))  # 默认表示未更新
    # chapter_state=Column(String(10),default='1')
    # matter_state=Column(String(10),default='1')
    # bespoke_state=Column(String(10),default='1')


class RETRUNOPTION(Base):
    __tablename__ = 'yctreturnoption'
    id = Column(Integer, primary_key=True)
    yctAppNo = Column(String(50))
    other_content = Column(String(1000))
    company_name = Column(String(1000))
    engage_range_repair = Column(String(1000))


Base.metadata.create_all(engine)

# Base.create_all()
