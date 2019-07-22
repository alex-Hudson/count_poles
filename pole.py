from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from globals import Base

class Pole(Base):
    __tablename__ = 'pole'
    __table_args__ = {'schema':'data'}

    id = Column(Integer, primary_key=True)
    telco_pole_tag = Column(String)

    def __repr__(self):
        return "<Pole(id='%s', telco_pole_tag='%s')>" % (self.id, self.telco_pole_tag)