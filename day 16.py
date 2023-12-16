import os
import logging
import collections
def tiskni_mapu(mapa):
    for line in mapa:
        print(line)
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
        mapa_stran['north']['from']: [{'to': mapa_stran['south']['to']}],
        mapa_stran['south']['from']: [{'to': mapa_stran['north']['to']}],
        mapa_stran['east']['from']: [{'to': mapa_stran['north']['to'], }, {'to': mapa_stran['south']['to']}],
        mapa_stran['west']['from']: [{'to': mapa_stran['north']['to'], }, {'to': mapa_stran['south']['to']}]
    },
    '-':{
        mapa_stran['north']['from']: [{'to': mapa_stran['east']['to']},{'to': mapa_stran['west']['to']}],
        mapa_stran['south']['from']: [{'to': mapa_stran['east']['to']},{'to': mapa_stran['west']['to']}],
        mapa_stran['east']['from']: [{'to': mapa_stran['west']['to'], }],
        mapa_stran['west']['from']: [{'to': mapa_stran['east']['to'], }]
    },
    #- is a horizontal pipe connecting east and west.
    '/':{
        mapa_stran['north']['from']: [{'to': mapa_stran['west']['to']}],
        mapa_stran['south']['from']: [{'to': mapa_stran['east']['to']}],
        mapa_stran['east']['from']: [{'to': mapa_stran['south']['to']}],
        mapa_stran['west']['from']: [{'to': mapa_stran['north']['to']}]
    },
    '\\':{
        mapa_stran['north']['from']: [{'to': mapa_stran['east']['to']}],
        mapa_stran['south']['from']: [{'to': mapa_stran['west']['to']}],
        mapa_stran['east']['from']: [{'to': mapa_stran['north']['to']}],
        mapa_stran['west']['from']: [{'to': mapa_stran['south']['to']}]
    },
    '.':{
        mapa_stran['north']['from']: [{'to': mapa_stran['south']['to']}],
        mapa_stran['south']['from']: [{'to': mapa_stran['north']['to']}],
        mapa_stran['east']['from']: [{'to': mapa_stran['west']['to'], }],
        mapa_stran['west']['from']: [{'to': mapa_stran['east']['to'], }]
    }
}
def vypocitej_coord(mapa,point_from,offset_to):
    new_point =  (point_from[0]+offset_to[0],point_from[1]+offset_to[1])
    if new_point[0] < 0 or new_point[1] < 0 or new_point[0] == len(mapa) or new_point[1] == len(mapa[0]):
        return None
    return new_point
def vypocitej_smer(point_from,point_to):
    return (point_to[0]-point_from[0], point_to[1]-point_from[1])
def walk_it(mapa,mapa_navstiveni,point_actual,point_from):
    zasobnik_cache = set()
    zasobnik = set()
    zasobnik.add(tuple([tuple(point_actual),tuple(point_from)]))
    while zasobnik:
        (point_actual, point_from) = zasobnik.pop()
        mapa_navstiveni[point_actual[0]][point_actual[1]] = '#'
        instrukce = mapa[point_actual[0]][point_actual[1]]
        direction_from = vypocitej_smer(point_from,point_actual)
        if True:
            point_from_candidate = point_actual
            for smer_to in mapa_kroku[instrukce][direction_from]:
                point_actual_candidate = vypocitej_coord(mapa,point_actual,smer_to['to'])
                # Otestuj zda uz to je v cache, jinak strcit do zasobniku
                if point_actual_candidate and tuple([tuple(point_actual_candidate),tuple(point_from_candidate)]) not in zasobnik_cache:
                    zasobnik.add(tuple([tuple(point_actual_candidate),tuple(point_from_candidate)]))
        zasobnik_cache.add(tuple([tuple(point_actual),tuple(point_from)]))
                
        
def walk_it_orig(mapa,mapa_navstiveni,point_actual,point_from):
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
def zpracuj_mapu(mapa):
    mapa_navstiveni = [['.'] * len(mapa[0]) for _ in range(len(mapa))]
    walk_it(mapa,mapa_navstiveni,[0,0],[0,-1])
    vysledek_part1 = 0
    for line in mapa_navstiveni:
        vysledek_part1 += line.count('#')
    return (vysledek_part1,None)
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
            mapa.append(line)
    
    (vysledek_part1, vysledek_part2) = zpracuj_mapu(mapa)
    #tiskni_mapu(mapa_navstiveni)
    
    print(f'Vysledek Part 1: {vysledek_part1}')
if __name__ == '__main__':
    main()