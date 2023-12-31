# uvicorn fastapi_test:app --reload
from fastapi import FastAPI, HTTPException, File, UploadFile
from sqlalchemy import create_engine, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy import DateTime
from datetime import datetime
from database import *
from sqlalchemy import LargeBinary
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse,FileResponse
import shutil
import os
from fastapi import Form, UploadFile
import json
from sqlalchemy.orm import Session
from fastapi import Depends
# FastAPI 애플리케이션 생성
app = FastAPI()
# CORS 설정 추가
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5500",# FastAPI 서버 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# SQLite 데이터베이스 연결 설정
DATABASE_URL = "sqlite:///./tmp5.db"
engine = create_engine(DATABASE_URL)

# 데이터베이스 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델 생성
Base = declarative_base()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class UploadedFile(Base):
    __tablename__ = "uploaded_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    
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
    FILE_NAME = Column(String, index=True)
    URL = Column(String, index=True, default=None)
    TIME = Column(String, index=True, default= None)
    DATE = Column(DateTime, default=datetime.utcnow, nullable=False)
    customers = relationship("Customer", back_populates="musics")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
# 테이블 생성
Base.metadata.create_all(bind=engine) 


@app.post("/upload/")
async def upload_file(pdfFile: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, pdfFile.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(pdfFile.file, f)

        db_file = UploadedFile(filename=pdfFile.filename)
        db.add(db_file)
        db.commit()

        return JSONResponse(content={"message": "파일 업로드 및 데이터베이스 저장 완료"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

@app.get("/files/")
async def get_files(db: Session = Depends(get_db)):
    files = db.query(UploadedFile).all()
    return files

@app.get("/download/{file_id}")
async def download_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(UploadedFile).filter(UploadedFile.id == file_id).first()

    if file:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        return FileResponse(file_path)
    else:
        return JSONResponse(content={"message": "파일을 찾을 수 없습니다."}, status_code=404)


# 라우터 설정
@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPId"}


@app.get("/hi")
async def read_root():
    return {"message": "Hello, FastAPIasdfasdfasfas"}

# 테스트용 API 엔드포인트
@app.get("/test-database-connection")
async def test_database_connection():
    try:
        engine.connect()
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"error": str(e)}
    
@app.put("/test_input")
def insert_data():
    session = SessionLocal()

    data = {
        "ID": "example_id",
        "PWD": "example_pwd",
        "PHONE_NUM": "123-456-7890",
        "E_MAIL": "example@example.com"
    }

    existing_user = session.query(Customer).filter(Customer.ID == data["ID"]).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="ID already exists")  # 409 Conflict

    session.add(Customer(**data))
    session.commit()
    session.close()
    return {"message": "Data insertion is complete"}

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

# @app.post("/set_music")
# def set_music(data: dict):
#     try:
#         # 데이터베이스 연결
#         session = SessionLocal()
#         session.add(Music(**data))
#         session.commit()

#         session.close()

#         return {"message": "setting save complete"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
@app.post("/set_music")
def set_music(data: dict):
    print("recive data",data)
    try:
        # 데이터베이스 연결
        session = SessionLocal()
        
        music_data = {
            'CUS_NO': data['CUS_NO'],
            'FILE_NAME': data['FILE_NAME'],
            'URL': data['URL'],
            'TIME': data['TIME']
        }
        session.add(Music(**music_data))
        session.commit()

        session.close()

        return {"message": "setting save complete"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/insert")
def sign_up(data: dict):
    session = SessionLocal()
    existing_user = session.query(Customer).filter(Customer.ID == data["ID"]).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="ID already exists")  # 409 Conflict
    session.add(Customer(**data))
    session.commit()
    session.close()
    return {"message": "Sign up is complete"}


@app.post("/login")
def login(data:dict):
    session = SessionLocal()
    user = session.query(Customer).filter(Customer.ID == data["ID"], Customer.PWD == data["PWD"]).first()
    session.close()
    if user:
        return {"message": "로그인 성공", "ID": user.ID, "CUS_NO": user.NO}
    else:
        raise HTTPException(status_code=401, detail="로그인 실패")


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)