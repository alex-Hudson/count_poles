from globals import Base, Session
from pole import Pole


class GasSupplyArea(Base):
    __tablename__ = 'gas_supply_area'
    __table_args__ = {
        'schema':'data',
        'autoload': True,
        'autoload_with': Session.bind 
    }
    
    def __repr__(self):
        ## string representation of self
        return "{}(id={})".format(self.__class__.name, self.name)

    def n_within(self,model):
        ## number of features of type model within self's boundary
        ##
        ## MODEL must have a geometry field called the_geom 
        pred = model.the_geom.ST_CoveredBy(self.boundary)
        return int( Session.query(model).filter( pred ).count() )
        