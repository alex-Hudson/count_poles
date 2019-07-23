import sqlalchemy 
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect 
from sqlalchemy.orm import sessionmaker
import argparse
import sys
import json
import geoalchemy2
import shapely
from shapely.geometry import shape

def main():
    import globals

    # Read polygons (and error check)
    try:
        with open('test.json') as json_file:
            polygon_geoms = json.load(json_file)
    except IOError as cond:
        print 'error reading from file:',cond
        exit(1)


    # Open database
    engine = sqlalchemy.create_engine('postgresql://postgres:Ubi2011sense@localhost:5432/{db_name}'.format(db_name='myw_dev'))
    globals.Session = sessionmaker(bind=engine)()

    # import models
    from pole import Pole
    from gas_supply_area import GasSupplyArea

    results = {}
    # for each polygon count poles inside
    for name,polygon_json in polygon_geoms.iteritems():
        n_poles=0
        poly = shape(polygon_json)
        poly_wkb_el = geoalchemy2.shape.from_shape(poly,srid=4326)
        pred = Pole.the_geom.ST_CoveredBy(poly_wkb_el)
        results[name] = int(globals.Session.query(Pole).filter( pred ).count())

    print 'FROM FILE\npolygon\tpoles\n-------\t-----'
    for k,n_poles in results.iteritems():
        print '{}\t{}'.format(k, n_poles)

    supply_areas = globals.Session.query(GasSupplyArea).filter(GasSupplyArea.name=='CB24')
    
    results = {}
    # for each polygon count poles inside
    for supply_area in supply_areas:
        results[supply_area.name] = supply_area.n_poles()

    print '\nFROM DATABASE\npolygon\tpoles\n-------\t-----'
    for k,n_poles in results.iteritems():
        print '{}\t{}'.format(k, n_poles)

main()