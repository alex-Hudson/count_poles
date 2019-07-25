# Command line utility to return models passed in as arg
import sys
import json
import geoalchemy2
from shapely.geometry import shape
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import pandas as pd



def main():
    ##
    # Command line tool to query number of models within an area 
    # Areas are defined in a file
    ##

    # Format args
    (db_name, poly_file, feature_type_spec) = sys.argv[-3:]

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
    
    # Get feature types and models without geometry
    feature_types = []
    models = []
    for feature_type in db.dd.featureTypes('myworld', feature_type_spec):
        model = db.dd.featureModel(feature_type)
        if not model._descriptor.primary_geom_field:
            print 'no geometry field'
            continue
        models.append(model)
        feature_types.append(feature_type)     
    
    if not feature_types:
        print 'no features'
        exit(1)
        
    # for each polygon count features inside
    results = {}
    for model in models:
        model_name    = model._descriptor.name
        results[model_name] = {}
        poly_results = {}
        for name,polygon_json in polygon_geoms.items():
            poly        = shape(polygon_json)
            poly_wkb_el = geoalchemy2.shape.from_shape(poly,srid=4326)
            geom_col      = getattr(model,model._descriptor.primary_geom_field.name)
            pred          = geom_col.ST_CoveredBy(poly_wkb_el)
            poly_results[name] = int(Session.query(model).filter( pred ).count())
        results[model_name].update(poly_results)
    
    # print results         
    feature_ids = []
    frames = []
    for feature_id, d in results.items():
        feature_ids.append(feature_id)
        frames.append(pd.DataFrame.from_dict(d, orient='index'))

    df = pd.concat(frames, axis = 1).T.drop_duplicates().T
    df.columns = feature_types

    print df

    # exit()

    # # print results
    # for model in models:
    #     model_name = model._descriptor.name
    #     width = len(model_name)
    #     print 'polygon\t{feature_type}'.format(feature_type=model_name)
    #     print '-------\t{:{fill}{align}{width}}'.format('',fill='-',align='<',width=width)
    #     for k,n_features in results[model_name].items():
    #         print '{}\t{}'.format(k, n_features)


main()