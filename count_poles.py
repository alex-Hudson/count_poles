import sqlalchemy 
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect 
from sqlalchemy.orm import sessionmaker
import argparse
import sys
import json


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
            polygon_geom = json.load(json_file)
    except:
        print 'error reading from file'
        raise IOError


    # Open database
    engine = sqlalchemy.create_engine('postgresql://postgres:Ubi2011sense@localhost:5432/{db_name}'.format(db_name=args.db_name))
    globals.Session = sessionmaker(bind=engine)()
    print globals.Session
    # import models
    from pole import Pole

    # for each polygon
        # count poles inside polygon 

    # print results


    for rec in globals.Session.query(Pole):
        print rec.id, rec.telco_pole_tag, rec.the_geom

main()