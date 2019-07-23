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
print(args.db_name, args.json_file)


def main():
    #from globals import Session
    import globals

    # Read polygons (and error check)
    try:
        with open(args.json_file) as json_file:
            polygon_geoms = json.load(json_file)
    except error as cond:
        print 'error reading from file:',cond
        exit(1)


    # Open database
    engine = sqlalchemy.create_engine('postgresql://postgres:Ubi2011sense@localhost:5432/{db_name}'.format(db_name=args.db_name))
    globals.Session = sessionmaker(bind=engine)()

    # import models
    from pole import Pole

    results = {}
    # for each polygon
    for name,poly_json in polygon_geoms.iteritems():
        poly = shape(poly_json)
        
        # For each pole ... check if it is inside inside polygon
        n_poles = 0
        
        for rec in globals.Session.query(Pole):

            # Get geom as shapely
            pnt = geoalchemy2.shape.to_shape( rec.the_geom )

            # Do test
            if poly.contains(pnt):
                
                n_poles += 1
        
        results[name] = {}
        results[name]['n_poles'] = n_poles


    print 'polygon\tpoles\n-------\t-----'
    for k,v in results.iteritems():
        print '{}\t{}'.format(k, v['n_poles'])



    

main()