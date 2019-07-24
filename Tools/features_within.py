# Command line utility to return models passed in as arg
import sys
import json
import geoalchemy2
from shapely.geometry import shape
import sqlalchemy
from sqlalchemy.orm import sessionmaker



def main():
    ##
    # Command line tool to query number of models within an area 
    # Areas are defined in a file
    ##

    # Format args
    (db_name, poly_file, feature_type) = sys.argv[-3:]

    # Open Session
    engine = sqlalchemy.create_engine('postgresql://postgres:Ubi2011sense@localhost:5432/{db_name}'.format(db_name=db_name))
    Session = sessionmaker(bind=engine)()

    # Read polygons (and error check)
    try:
        with open('../' + poly_file) as json_file: # polygon file saved in parent dir
            polygon_geoms = json.load(json_file)
    except IOError as cond:
        print 'error reading from file:',cond
        exit(1)
    
    # Get name of column with geom
    model = db.dd.featureModel(feature_type)
    for column in  model.__table__.c:
        if 'geometry' in str(column.type):
            geom_col_name = column.name

    # if no column with geometry is found, set column to None
    try: geom_col_name
    except NameError: geom_col_name = None
    
    # for each polygon count poles inside
    results = {}
    for name,polygon_json in polygon_geoms.iteritems():
        n_features=0
        if geom_col_name is not None:
            poly = shape(polygon_json)
            poly_wkb_el = geoalchemy2.shape.from_shape(poly,srid=4326)
            geom_col = getattr(model, geom_col_name)
            pred = geom_col.ST_CoveredBy(poly_wkb_el)
            results[name] = int(Session.query(model).filter( pred ).count())
        else:
            results[name] = n_features

    # print results
    width = len(feature_type)
    print 'polygon\t{feature_type}'.format(feature_type=feature_type)
    print '-------\t{:{fill}{align}{width}}'.format('',fill='-',align='<',width=width)
    for k,n_poles in results.iteritems():
        print '{}\t{}'.format(k, n_poles)


main()