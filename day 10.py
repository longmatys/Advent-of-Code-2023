import os
import logging
import collections
import itertools
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
#| is a vertical pipe connecting north and south.
mapa_kroku = {
    '|':{
        mapa_stran['north']['from']: {'to': mapa_stran['south']['to'], 'smer': 'rovne'},
        mapa_stran['south']['from']: {'to': mapa_stran['north']['to'], 'smer': 'rovne'}
    },
    #- is a horizontal pipe connecting east and west.
    '-':{
        mapa_stran['east']['from']: {'to': mapa_stran['west']['to'], 'smer': 'rovne'},
        mapa_stran['west']['from']: {'to': mapa_stran['east']['to'], 'smer': 'rovne'}
    },
    #L is a 90-degree bend connecting north and east.
    'L':{
        mapa_stran['north']['from']: {'to': mapa_stran['east']['to'], 'smer': 'left'},
        mapa_stran['east']['from']: {'to': mapa_stran['north']['to'], 'smer': 'right'}
    },
    #J is a 90-degree bend connecting north and west.
    'J':{
        mapa_stran['north']['from']: {'to': mapa_stran['west']['to'], 'smer': 'right'},
        mapa_stran['west']['from']: {'to': mapa_stran['north']['to'], 'smer': 'left'}
    },
    #7 is a 90-degree bend connecting south and west.
    '7':{
        mapa_stran['south']['from']: {'to': mapa_stran['west']['to'], 'smer': 'left'},
        mapa_stran['west']['from']: {'to': mapa_stran['south']['to'], 'smer': 'right'}
    },
    #F is a 90-degree bend connecting south and east.
    'F':{
        mapa_stran['south']['from']: {'to': mapa_stran['east']['to'], 'smer': 'right'},
        mapa_stran['east']['from']: {'to': mapa_stran['south']['to'], 'smer': 'left'}
    },
}
#. is ground; there is no pipe in this tile.
#S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
def vypocitej_coord(mapa,point_from,offset_to):
    new_point =  (point_from[0]+offset_to[0],point_from[1]+offset_to[1])
    if new_point[0] < 0 or new_point[1] < 0 or new_point[0] == len(mapa) or new_point[1] == len(mapa[0]):
        return None
    return new_point
def vypocitej_smer(point_from,point_to):
    return (point_to[0]-point_from[0], point_to[1]-point_from[1])
def vypocitej_volno_pro_smer(mapa,mapa_navstiveni,point_actual,smer_zatacky):
    if smer_zatacky == 'rovne':
        return
    for smer in ['west','east','north','south']:
        new_point = vypocitej_coord(mapa,point_actual,mapa_stran[smer].get('from'))
        if new_point:
            instrukce = mapa_navstiveni[new_point[0]][new_point[1]]
            if instrukce == False:
                mapa_navstiveni[new_point[0]][new_point[1]] = smer_zatacky
def flood_it(mapa,mapa_navstivenosti,smer_zatacky):
    seznam = set()
    for i,line in enumerate(mapa_navstivenosti):
        for j,bod in enumerate(line):
            if bod==smer_zatacky:
                seznam.add((i,j))
        #t  = [{i,j} for j,bod in enumerate(line) if bod==smer_zatacky]
        #seznam.add(t)
    while (len(seznam)):
        point_actual = seznam.pop()
        
        for smer in mapa_stran.keys():
            new_point = vypocitej_coord(mapa_navstivenosti,point_actual,mapa_stran[smer].get('from'))
            if new_point:
                instrukce = mapa_navstivenosti[new_point[0]][new_point[1]]
                #if instrukce == False and mapa[new_point[0]][new_point[1]]=='.':
                if instrukce == False:
                    mapa_navstivenosti[new_point[0]][new_point[1]] = smer_zatacky
                    seznam.add((new_point[0],new_point[1]))
    
def walk_it(mapa,mapa_navstiveni,point_actual,point_from):
    step_counter = 0
    smery = []
    
    while True:
        mapa_navstiveni[point_actual[0]][point_actual[1]] = True
        instrukce = mapa[point_actual[0]][point_actual[1]]
        if point_from == None:
            logging.debug('Zacinam prochazet trubky a hledam varianty')
            for go_from,go_to in [['west','east'],['east','west'],['north','south'],['south','north']]:
                #if mapa_kroku[go_from].get(go_to):
                new_point = vypocitej_coord(mapa,point_actual,mapa_stran[go_from].get('from'))
                if new_point:
                    #bod je platny, jsem stale uvnitr mapy
                    instrukce = mapa[new_point[0]][new_point[1]]
                    if mapa_kroku[instrukce].get(mapa_stran[go_from]['from']) is not None:
                        #na pristim miste je trubka, ktera se napojuje na soucasnou pozici
                        step_counter += 1
                        point_from = point_actual
                        point_actual = new_point
                        break
                        
                        #return 1 + walk_it(mapa,new_point,point)
        elif instrukce == 'S' and step_counter > 0:
            smery_counter = collections.Counter(smery)
            return [step_counter,smery_counter]
        else:
            if point_actual == (4,15):
                print(1)
            direction_from = vypocitej_smer(point_from,point_actual)
            
            step_counter += 1
            vypocitej_volno_pro_smer(mapa,mapa_navstiveni,point_actual,mapa_kroku[instrukce][direction_from]['smer'])
            point_from = point_actual
            point_actual = vypocitej_coord(mapa,point_actual,mapa_kroku[instrukce][direction_from]['to'])
            smery.append(mapa_kroku[instrukce][direction_from]['smer'])
            #vypocitej_volno_pro_smer(mapa,mapa_navstiveni,point_actual,mapa_kroku[instrukce][direction_from]['smer'])
            logging.debug(f"Jsem na {point_from} - {instrukce} a chci jit na{point_actual}")
def spocitej_vnitrni_prostory(mapa_navstiveni):
    counter = 0
    for i,line in enumerate(mapa_navstiveni):
        logging.debug(f'Prochazim linku {line}')
        uvnitr = False
        candidate = 0
        bod_last = line[0]
        for j,bod in enumerate(line):
            if bod:
                counter+=candidate
                candidate=0
                if not bod_last:
                    uvnitr = not uvnitr
                    bod_last = bod
            else:
                if uvnitr:
                    candidate+=1
    """
    for i in range(len(mapa_navstiveni[0])):
        uvnitr = False        
        for j in range(len(mapa_navstiveni)):
            bod = mapa_navstiveni[j][i]
            if bod:
                uvnitr = not uvnitr
            else:
                if uvnitr:
    """
                    
    return counter
def tiskni_mapu(mapa):
    for line in mapa:
        print(line)
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    mapa = []
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '#':
                break
            if line.find('S') >= 0:
                point = [len(mapa),line.find('S')]
            mapa.append(line)
            logging.debug(line)
    logging.debug(f'Nasel jsem startovni bod {point}')
    mapa_navstiveni = [[ False for _ in range(len(mapa[0])) ] for _ in range(len(mapa))]
    [delka_cele_cesty,smery] = walk_it(mapa,mapa_navstiveni,point,None)
    print(f'Usel jsem celou cestu v delce {delka_cele_cesty} -> odpoved je tedy {delka_cele_cesty/2}')
    
    flood_it(mapa,mapa_navstiveni,'right')
    flood_it(mapa,mapa_navstiveni,'left')
    vnitrni_smer = collections.Counter([t for t in smery.keys() if t == 'left' or t=='right' ]).most_common(2)[1]
    vnitrni_smer = [t for t in smery.most_common(3) if t[0] == 'left' or t[0] =='right'][1]
    vnitrek = collections.Counter(itertools.chain.from_iterable(mapa_navstiveni))[vnitrni_smer[0]]
    print(f'Uvnitr je {vnitrek} prostoru')
    #tiskni_mapu(mapa)
    #tiskni_mapu(mapa_navstiveni)
    #1241 is too high
if __name__ == '__main__':
    main()