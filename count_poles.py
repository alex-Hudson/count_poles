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

# Define signature
arg_parser = argparse.ArgumentParser(add_help=False)
arg_parser.add_argument('db_name', type=str, help="database name")
arg_parser.add_argument('json_file', type=str, help="GeoJSPON polygons keyed by name")


# Parse command line
args = arg_parser.parse_args(sys.argv[1:])


def main():
    import globals

    # Read polygons (and error check)
    try:
        with open(args.json_file) as json_file:
            polygon_geoms = json.load(json_file)
    except IOError as cond:
        print 'error reading from file:',cond
        exit(1)


    # Open database
    engine = sqlalchemy.create_engine('postgresql://postgres:Ubi2011sense@localhost:5432/{db_name}'.format(db_name=args.db_name))
    globals.Session = sessionmaker(bind=engine)()

    # import models
    from pole import Pole
    from gas_supply_area import GasSupplyArea

    supply_areas = globals.Session.query(GasSupplyArea)
    
    results = {}
    # for each polygon count poles inside
    for supply_area in supply_areas:
        results[supply_area.name] = supply_area.n_poles()

    print 'polygon\tpoles\n-------\t-----'
    for k,n_poles in results.iteritems():
        print '{}\t{}'.format(k, n_poles)


main()