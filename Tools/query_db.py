# Command line utility to return models passed in as arg
import sys
import argparse
import sys
import json
import geoalchemy2
import shapely
from shapely.geometry import shape


sys.path.append('../')

(poly_file, feature_type) = sys.argv[-2:]

model = db.dd.featureModel(feature_type)
for rec in db.session.query(model):
    print(rec)

# use count_poles.py to print out answer (copy and paste)

def main():
    import globals

    # Read polygons (and error check)
    try:
        with open(poly_file) as json_file:
            polygon_geoms = json.load(json_file)
    except IOError as cond:
        print 'error reading from file:',cond
        exit(1)
    
    # for each polygon count poles inside
    results = {}
    for name,polygon_json in polygon_geoms.iteritems():
        n_poles=0
        poly = shape(polygon_json)
        poly_wkb_el = geoalchemy2.shape.from_shape(poly,srid=4326)
        pred = model.the_geom.ST_CoveredBy(poly_wkb_el)
        results[name] = int(globals.Session.query(model).filter( pred ).count())

    # print results
    print 'polygon\tpoles\n-------\t-----'
    for k,n_poles in results.iteritems():
        print '{}\t{}'.format(k, n_poles)


main()