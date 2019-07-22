import sqlalchemy 
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect 
from sqlalchemy.orm import sessionmaker
import argparse
import sys


# Define signature
arg_parser = argparse.ArgumentParser(add_help=False)
arg_parser.add_argument('db_name', type=str, help="database name")
arg_parser.add_argument('json_file', type=str, help="GeoJSPON polygons keyed by name")


# Parse command line
args = arg_parser.parse_args(sys.argv[1:])
print(args.db_name, args.json_file)


def main():
    engine = sqlalchemy.create_engine('postgresql://postgres:Ubi2011sense@localhost:5432/{db_name}'.format(db_name=args.db_name))

    Session = sessionmaker(bind=engine)
    session = Session()

    from pole import Pole

    for record in session.query(Pole):
        print(record)

main()