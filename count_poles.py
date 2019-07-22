import sqlalchemy 
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect 
import argparse
import sys

# class CountPoles():
#     def __init__(self):

#     def get_database(self):


# Define signature
arg_parser = argparse.ArgumentParser(add_help=False)
arg_parser.add_argument('db_name', type=str, help="database name")

# Parse command line
args = arg_parser.parse_args(sys.argv[1:])
print(args.db_name)

metadata = MetaData()

engine = sqlalchemy.create_engine('postgresql://postgres:Ubi2011sense@localhost:5432/myw_dev')
poles = Table('data.poles', metadata, autoload = True, autoload_with = engine)

connection = engine.connect()
result = connection.execute("select * from data.pole")
for row in result:
    print("id:", row['id'], "telco_pole_tag", row['telco_pole_tag'])
connection.close()

# metadata.create_all(engine)
# inspector = inspect(engine)
# inspector.get_columns('data')


#poles = sqlalchemy.Table('data', metadata, autoload=True, autoload_with=engine)

# Equivalent to 'SELECT * FROM census'
query = sqlalchemy.select([poles])
print query

ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
print ResultSet[:3]

