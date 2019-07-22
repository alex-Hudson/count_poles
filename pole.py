from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from globals import Base, Session
from geoalchemy2 import Geometry


class Pole(Base):
    __tablename__ = 'pole'
    __table_args__ = {
        'schema':'data',
        'autoload': True,
        'autoload_with': Session.bind 
    }

    the_geom = Column(Geometry('POLYGON'))

 
    def __repr__(self):
        return "Pole(id={})".format(self.id)