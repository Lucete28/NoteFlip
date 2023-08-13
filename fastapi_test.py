# uvicorn fastapi_test:app --reload
from fastapi import FastAPI
from sqlalchemy import create_engine, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import DateTime
from datetime import datetime
from database import *
# FastAPI 애플리케이션 생성
app = FastAPI()

# SQLite 데이터베이스 연결 설정
DATABASE_URL = "sqlite:///tmp.db"
engine = create_engine(DATABASE_URL)

# 데이터베이스 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델 생성
Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    
    NO = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ID = Column(String, index=True)
    PWD = Column(String, index=True)
    PHONE_NUM = Column(String, index=True, default=None)
    E_MAIL = Column(String, index=True, default= None)
    musics = relationship("Music", back_populates="customers")
    
class Music(Base):
    __tablename__ = "musics"
    
    NO = Column(Integer, primary_key=True, index=True, autoincrement=True)
    CUS_NO = Column(Integer, ForeignKey("customers.NO"))
    NAME = Column(String, index=True)
    URL = Column(String, index=True, default=None)
    FILE = Column(String, index=True, default= None)
    TIME = Column(String, index=True, default= None)
    DATE = Column(DateTime, default=datetime.utcnow, nullable=False)
    customers = relationship("Customer", back_populates="musics")
    


# 라우터 설정
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPId"}


@app.get("/customer")
async def read_customer():
    session = SessionLocal()
    customers = session.query(Customer).all()
    session.close()
    return customers

@app.get("/music")
async def read_music():
    session = SessionLocal()
    musics = session.query(Music).all()
    session.close()
    return musics

@app.get("/music/{cus_no}")
def get_music_by_cus_no(cus_no: int):
    session = SessionLocal()
    music = session.query(Music).filter(Music.CUS_NO == cus_no).all()
    session.close()
    return music


@app.post("/insert")
def sign_up(data: dict):
    session = SessionLocal()
    session.add(Customer(**data))
    session.commit()
    session.close()
    return {"message": "Sign up is complete"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
