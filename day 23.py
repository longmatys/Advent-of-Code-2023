import os
import logging
import sys
sys.setrecursionlimit(10000)
mapa_stran = {
    'south': {
        'from': (-1,0),
        'to': (1,0)
    },
    'west': {
        'from': (0,1),
        'to': (0,-1)
    },
    'east': {
        'from': (0,-1),
        'to': (0,1)
    },
    'north': {
        'from': (1,0),
        'to': (-1,0)
    }
}
mapa_instrukci = {
    '>': [mapa_stran['east']['to']],
    '<': [mapa_stran['west']['to']],
    '^': [mapa_stran['north']['to']],
    'v': [mapa_stran['south']['to']],
    '.': [mapa_stran['east']['to'], mapa_stran['south']['to'], mapa_stran['west']['to'], mapa_stran['north']['to']]
}
def vypocitej_coord(mapa,point_from,offset_to):
    new_point =  (point_from[0]+offset_to[0],point_from[1]+offset_to[1])
    if new_point[0] < 0 or new_point[1] < 0 or new_point[0] == len(mapa) or new_point[1] == len(mapa[0]):
        return None
    return new_point
def walk_it(mapa:list,historie:set,point_actual:tuple,point_cil:tuple):
    step_counter = 0
    smery = []
    
    
    historie.add(point_actual)
    instrukce = mapa[point_actual[0]][point_actual[1]]
    if instrukce == '#':
        historie.remove(point_actual)
        return None
    if point_actual == point_cil:
        historie.remove(point_actual)
        return 0
    ret_value = None
    for smer in mapa_instrukci[instrukce]:
        new_point = vypocitej_coord(mapa,point_actual,smer)
        if new_point:
            if new_point not in historie and mapa[new_point[0]][new_point[1]] != '#':
                #bod je platny, jsem stale uvnitr mapy
                vysledek = walk_it(mapa,historie,new_point,point_cil)
                if vysledek is not None and (ret_value is None or vysledek > ret_value):
                    ret_value = vysledek
            else:
                #historie.remove(point_actual)
                continue
    historie.remove(point_actual)
    if ret_value is None:
        return None
    return ret_value + 1
         
def main():
    mapa = []
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            mapa.append(line)
    vysledek = walk_it(mapa,set(),tuple([0,mapa[0].find('.')]),tuple([len(mapa)-1,mapa[-1].find('.')]))
    print(vysledek)
if __name__ == '__main__':
    main()