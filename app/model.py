from sqlalchemy import Column,Integer,String,Float
from .database import Base

class Travel(Base):
    __tablename__ = "Country"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String,nullable=False)
    city = Column(String,nullable=False)
    duration = Column(Integer,nullable=False)
    cost = Column(Integer,nullable=False)
