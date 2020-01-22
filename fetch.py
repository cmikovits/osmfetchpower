#!/usr/bin/python3

import click
import logging
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim
from collections import OrderedDict
import itertools
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
    lat = e.lat()
    lon = e.lon()
    if (e.type()=='way' or e.type() == 'relation'):
        if (e.type()=='relation'):
            polys = e.geometry()['coordinates']
            points = []
            for p in polys:
                p = p[0]
                points = points + p
        else:
            points = e.geometry()['coordinates'][0]
        lat = []
        lon = []
        
        # loop if there is more than one point (lat/lon) tuple
        depth = lambda L: isinstance(L, list) and max(map(depth, L))+1
                                                      
        logging.debug("cols: %s, rows: %s", len(points), depth(points))
        
        if (depth(points) > 1):
            for p in points:
                lat.append(p[0])
                lon.append(p[1])
            lat = sum(lat)/len(lat)
            lon = sum(lon)/len(lon)
        else:
            lat = points[0]
            lon = points[1]
    if (e.type()=='relation'):
        polys = e.geometry()['coordinates']
        points = []
        for p in polys:
            p = p[0]
            points = points + p
        
        
    edict = {'id': e.id(), 'lat':lat, 'lon':lon, 'timestamp':e.timestamp(), **e.tags()}
    dfr = pd.DataFrame([edict])
    #print(dfr)
    df = pd.concat([df,dfr], axis=0, ignore_index=True, sort=False)
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
@click.option('-area', '-a', help='area input', default='Vienna', type=str)
@click.option('-loglevel', '-l', help='log level (INFO, DEBUG)', default='DEBUG', type=str)
def main(area, loglevel):
    logging.basicConfig(format='%(asctime)s, %(message)s',
                       datefmt='%Y-%m-%d %H:%M:%S')
    logging.getLogger().setLevel(loglevel)

    nominatim = Nominatim()
    areaId = nominatim.query(area).areaId()
    
    logging.debug("area: %s, id: %s",area,areaId)
    selectors = {'power':
                    ['plant','generator']
                 }
    
    df = pd.DataFrame()
    
    for osmkey, osmvalues in selectors.items():
        for osmval in osmvalues:
            logging.debug("fetching %s = %s",osmkey, osmval)
            data = fetchFeatures(areaId, osmkey, osmval)
            logging.debug("Number of Elements: %s", data.countElements())
            for i in range(0, data.countElements()):
                e = data.elements()[i]
                if (e.tag('type')=='site'):
                    print('site')
                    continue
                
                # id, lat, lon, timestamp, tags
                
                df = addFeaturetoGDF(df, e)
                
                #if getfirstrev:
                #    if (data.elements()[i].version() > 1):
                #        ne = fetchFeatureVersion(e.id(), 1)
    print(df)
    df.to_csv(r'test.csv')                

if __name__ == "__main__":
    main()
