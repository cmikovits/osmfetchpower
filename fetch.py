#!/usr/bin/python

import click
import logging
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass


overpass = Overpass()
query = overpassQueryBuilder(area=areaId, elementType='node', selector='"natural"="tree"', out='count')
result = overpass.query(query)
result.countElements()

@click.command()
@click.option('-country', '-c', help='country input', default='LU', type=str)
@click.option('-loglevel', '-l', help='log level', default='DEBUG', type=str)
def main(country, loglevel):
    logging.basicConfig(level=logging.)
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--country')
    country =  parser.parse_args().country
    print('Country:{}'.format(country))
    print('fetching plants')
    st = time.time()
    nodes, ways, rels = getfeatures(country, "power", "plant")
    features = nodes + ways + rels
    et = time.time()
    print('waiting for {:.0f} seconds'.format(et - st))
    time.sleep(et - st)
    print('fetching generators')
    nodes, ways, rels = getfeatures(country, "power", "generator")
    features = features + nodes + ways + rels

    writeshape(features, country)

if __name__ == "__main__":
    main()
