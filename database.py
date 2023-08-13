from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy import text
from sqlalchemy import DateTime
from datetime import datetime
import pytz

DATABASE_URL = "sqlite:///tmp.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"
    
    NO = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ID = Column(String, index=True)
    PWD = Column(String, index=True)
    PHONE_NUM = Column(String, index=True, default=None)
    E_MAIL = Column(String, index=True, default=None)
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

def get_customer_data():
    session = SessionLocal()
    customers = session.query(Customer).all()
    session.close()
    return customers

def do_query(query):
    session = SessionLocal()
    result = session.execute(query)
    session.commit()
    session.close()
    return result
# if __name__ == "__main__":
#     Base.metadata.create_all(bind=engine)

# # query = text("INSERT INTO customers (ID, PWD, PHONE_NUM, E_MAIL) VALUES ('Lucete', 'wjdghdus1!', '01039972802', '2580jhy@naver.com')")
# query = text("SELECT * FROM customers")
# print(do_query(query))