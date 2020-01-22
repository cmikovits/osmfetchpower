#!/usr/bin/python3

import click
import logging
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim
from collections import OrderedDict
import time
import pandas as pd
import geopandas as gpd

def fetchFeatures(areaId, osmkey, osmtype):
    overpass = Overpass()

    query = overpassQueryBuilder(area=areaId,
                                 elementType=['node', 'way', 'relation'],
                                 selector='"' + osmkey + '"="' + osmtype + '"',
                                 includeGeometry=True,
                                 out='center meta')
    logging.debug("OSM query: %s", query)
    return overpass.query(query, timeout=60)

def fetchFeatureVersion(id, version):
    api = Api()
    return(api.query('node/' + str(id) + '/1'))
    
def addFeaturetoGDF(df, e):
    edict = {'id': e.id(), 'lat':e.lat(), 'lon':e.lon(), **e.tags()}
    print(edict)
    dfr = pd.DataFrame([edict])
    print(dfr)
    exit(0)
    #df.append({'lat':[e.lat()],
    #           'lon':[e.lon()],
    #          }, ignore_index=True)
    return(df)
    
def writeGEO(data, path, dataname):
    data.to_file(filename = os.path.join(path, 'geojson', dataname+'.geojson'), driver="GeoJSON")
    data.to_file(filename = os.path.join(path, 'shape', dataname+'.shp'), driver = 'ESRI Shapefile')
    data.to_file(filename = os.path.join(path, 'data.gpkg'), layer = dataname, driver = 'GPKG')
    return(0)

@click.command()
@click.option('-area', '-a', help='area input', default='Aschau', type=str)
@click.option('-loglevel', '-l', help='log level (INFO, DEBUG)', default='DEBUG', type=str)
def main(area, loglevel):
    logging.basicConfig(format='%(asctime)s, %(message)s',
                       datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(loglevel)

    nominatim = Nominatim()
    areaId = nominatim.query(area).areaId()
    
    logging.debug("area: %s, id: %s",area,areaId)
    selectors = {'power':'plant',
                 'power':'generator'
                 }
    
    df = pd.DataFrame()
    
    for osmkey, osmval in selectors.items(): 
        logging.debug("fetching %s = %s",osmkey, osmval)
        data = fetchFeatures(areaId, osmkey, osmval)
        logging.debug("Number of Elements: %s", data.countElements())
        for i in range(0, data.countElements()):
            e = data.elements()[i]
            # id, lat, lon, timestamp, tags
            print(dir(e))
            #addFeaturetoGDF(df, e)
            
            #if getfirstrev:
            #    if (data.elements()[i].version() > 1):
            #        ne = fetchFeatureVersion(e.id(), 1)
    print(df)                

if __name__ == "__main__":
    main()
