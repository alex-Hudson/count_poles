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
        return "Gas_supply_area(id={})".format(self.name)

    def n_poles(self):
        pred = Pole.the_geom.ST_CoveredBy(self.boundary)
        return int(Session.query(Pole).filter( pred ).count()) # only get poles contained by current polygon
        