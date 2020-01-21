#!/usr/bin/python3

import click
import logging
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim
from collections import OrderedDict
import time

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

    selectors = {'power': 'plant'}
    
    for osmkey, osmval in selectors.items(): 
        logging.debug("fetching %s = %s",osmkey, osmval)
        data = fetchFeatures(areaId, osmkey, osmval)
        logging.debug("Number of Elements: %s", data.countElements())
        for i in range(0, 1):# data.countElements()):
            e = data.elements()[i]
            print(dir(e))
            print(e.tags())
            print(e.nodes())
            #id = data.elements()[i].id()
            #print(data.elements()[i].id())
            #print(data.elements()[i].lat(), " ", data.elements()[i].lat())
            #print(data.elements()[i].tags())
            #print(data.elements()[i].timestamp())
            #if (data.elements()[i].version() > 1):
            #    nelement = fetchFeatureVersion(id, 1)
            #    print('older version: ', nelement.id())
            #    print(nelement.tags())
            #    print(nelement.lat(), " ", nelement.lat())
            #    print(nelement.timestamp())

if __name__ == "__main__":
    main()
