from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from globals import Base
from geoalchemy2 import Geometry


class Pole(Base):
    __tablename__ = 'pole'
    __table_args__ = {'schema':'data'}

    id = Column(Integer, primary_key=True)
    telco_pole_tag = Column(String)
    the_geom = Column(Geometry('POLYGON'))

    def definition(self):
        ##
        ## Return self in a serializable format
        ## 
        return {
            'id'                    : self.id,
            'drop_code'             : self.drop_code,
            'make_ready'            : self.make_ready,
            'usage'                 : self.usage,
            'construction_status'   : self.construction_status,
            'material_type'         : self.material_type,
            'extension_arm'         : self.extension_arm,
            'power_riser'           : self.power_riser,
            'telco_riser'           : self.telco_riser,
            'bond'                  : self.bond, 
            'catv_riser_height'     : self.catv_riser_height, 
            'catv_pole_tag'         : self.catv_pole_tag, 
            'power_pole_tag'        : self.power_pole_tag, 
            'telco_pole_tag'        : self.telco_pole_tag, 
            'account_code'          : self.account_code, 
            'installed_cost'        : self.installed_cost, 
            'ground_status'         : self.ground_status, 
            'photo'                 : self.photo, 
            'cables'                : self.cabels, 
            'equipment'             : self.equipment,
            'connected_routes'      : self.connected_routes, 
            'the_geom'              : self.the_geom 
        }

    def __repr__(self):
        return "<Pole(id='%s', telco_pole_tag='%s', the_geom=%s)>" % (self.id, self.telco_pole_tag, self.the_geom)