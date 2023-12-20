from sqlalchemy import Column, DateTime, Float
#from sqlalchemy.types import Integer, String, Float, DateTime
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class ItemDB(Base):
    __tablename__ ="btc_1m"
    Datetime = Column(DateTime, primary_key=True)
    Open= Column(Float)
    High= Column(Float)
    Low= Column(Float)
    Close= Column(Float)
    Volume= Column(Float)
    #id = Column(Integer, primary_key=True, index=True)
    #AdjClose= Column(Float)

"""class ItemDB(BaseModel):
    __tablename__ ="BTCUSD_1m"
    Datetime: datetime
    Open: float
    High: float
    Low: float
    Close: float 
    Volume: float"""