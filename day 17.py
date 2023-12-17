import os
import logging
import sys
import time
sys.setrecursionlimit(1000*10)
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
    
    mapa_stran['north']['from']: [{'to': mapa_stran['south']['to']}, {'to': mapa_stran['east']['to']},{'to': mapa_stran['west']['to']}],
    mapa_stran['south']['from']: [{'to': mapa_stran['east']['to']}, {'to': mapa_stran['north']['to']},{'to': mapa_stran['west']['to']}],
    mapa_stran['east']['from']: [{'to': mapa_stran['south']['to']}, {'to': mapa_stran['north']['to']},{'to': mapa_stran['west']['to']}],
    mapa_stran['west']['from']: [{'to': mapa_stran['south']['to']}, {'to': mapa_stran['east']['to']},{'to': mapa_stran['north']['to']}]
}
def vypocitej_coord(mapa,point_from,offset_to):
    new_point =  (point_from[0]+offset_to[0],point_from[1]+offset_to[1])
    if new_point[0] < 0 or new_point[1] < 0 or new_point[0] == len(mapa) or new_point[1] == len(mapa[0]):
        return None
    return new_point
def vypocitej_smer(point_from,point_to):
    return (point_to[0]-point_from[0], point_to[1]-point_from[1])
MAX_DELKA = 3
def walk_it_s_while(mapa,point_actual,point_from, delka, hloubka = 0, cena_cesty=0):
    #vysledky = {point_actual:mapa[point_actual[0]][point_actual[1]]}
    global global_best
    zasobnik_cache = {}
    zasobnik = []
    zasobnik.append([tuple(point_actual),tuple(point_from),delka,cena_cesty,tuple([tuple(point_from)])])
    while zasobnik:
        #item = sorted(zasobnik,key=lambda x: x[3])[0]
        (point_actual, point_from, delka, cena_cesty, cela_cesta) = zasobnik.pop()
        #zasobnik.remove(item)
        
        hodnota = mapa[point_actual[0]][point_actual[1]]
        if global_best and global_best < cena_cesty + int(hodnota):
            continue
        
        #print(f'Nasel jsem kandidata na cestu {cena_cesty + int(hodnota)}')
        if point_actual[0] == len(mapa)-1 and point_actual[1] == len(mapa[0])-1:
            #print(f'Nasel jsem kandidata na nejlepsi cestu {cena_cesty + int(hodnota)}')
            if not global_best or global_best > cena_cesty + int(hodnota):
                global_best = cena_cesty + int(hodnota)
                
            continue
                
                
        direction_from = vypocitej_smer(point_from,point_actual)
    
        point_from_candidate = point_actual
        best_vysledek = None
        for smer_to in mapa_kroku[direction_from]:
            #print(f"{' '*hloubka} {hloubka}:direction_from: {direction_from}, Smer_to: {smer_to}")    
            offset = 1
            if smer_to['to'] == direction_from:
                if delka == MAX_DELKA:
                    continue
                else:
                    offset += delka
            
            point_actual_candidate = vypocitej_coord(mapa,point_actual,smer_to['to'])
            
            if point_actual_candidate: 
                hodnota_candidate = int(mapa[point_actual_candidate[0]][point_actual_candidate[1]])
                klic = tuple([point_actual_candidate,point_actual,offset])
                if not zasobnik_cache.get(klic) or zasobnik_cache[klic][0] >= cena_cesty + hodnota_candidate:
                    
                    zasobnik.append([tuple(point_actual_candidate),tuple(point_from_candidate),offset,cena_cesty + hodnota_candidate,tuple(list(cela_cesta)+[tuple(point_actual)])])
                    zasobnik_cache[klic] = [cena_cesty + hodnota_candidate, tuple(list(cela_cesta)+[tuple(point_actual)])]
                    #vysledek_candidate = walk_it_recursive(mapa,point_actual_candidate,point_from_candidate,offset,hloubka+1,cena_cesty+int(hodnota))
                    #if not best_vysledek or (vysledek_candidate and best_vysledek>vysledek_candidate):
                    #    best_vysledek = vysledek_candidate
                #walk_cache[tuple([tuple(point_actual_candidate),tuple(point_from_candidate),offset])] = 0
        #print(f"{' '*hloubka} {hloubka}:vracim nejlepsi vysledek pro {point_actual}: {best_vysledek}")
    
    
    z = min([v[0] for k,v in zasobnik_cache.items() if k[0] == tuple([len(mapa)-1, len(mapa[0])-1])])
    
    return z
walk_cache = {}
def update_cache(klic,hodnota):
    if walk_cache.get(klic):
        if walk_cache.get(klic) <= hodnota:
            return False
    walk_cache[klic] = hodnota
    return True
global_best = None
def print_mapa(mapa,point_actual,point_from,hloubka):
    print('Mapa',hloubka)
    for x,line in enumerate(mapa):
        for y,znak in enumerate(line):
            if x == point_actual[0] and y == point_actual[1]:
                print('*',end='')
            elif x == point_from[0] and y == point_from[1]:
                print('.',end='')
            else:
                print(znak,end='')
        print('')
    print('')
def walk_it_recursive(mapa,point_actual,point_from, delka, hloubka = 0, cena_cesty=0):
    global global_best
    hodnota = mapa[point_actual[0]][point_actual[1]]
    if not update_cache(tuple([tuple(point_actual),tuple(point_from),delka]),cena_cesty) or (global_best and global_best < cena_cesty + int(hodnota)):
        return None
    #print_mapa(mapa,point_actual,point_from,f'Hloubka: {hloubka}, cena_cesty:{cena_cesty}')
    #vysledky = {point_actual:mapa[point_actual[0]][point_actual[1]]}
    #zasobnik_cache = set()
    #zasobnik = set()
    #zasobnik.add(tuple([tuple(point_actual),tuple(point_from), delka]))
    #print(f"{' '*hloubka} {hloubka}:Prochazim bod {point_actual}")
    
    if point_actual[0] == len(mapa)-1 and point_actual[1] == len(mapa[0])-1:
        if not global_best or global_best > cena_cesty + int(hodnota):
            global_best = cena_cesty + int(hodnota)
        #print(f'Nasel jsem cestu: global_best:{global_best}, actual_best:{cena_cesty + int(hodnota)}')
        return int(hodnota)
    direction_from = vypocitej_smer(point_from,point_actual)
    
    point_from_candidate = point_actual
    best_vysledek = None
    for smer_to in mapa_kroku[direction_from]:
        #print(f"{' '*hloubka} {hloubka}:direction_from: {direction_from}, Smer_to: {smer_to}")    
        offset = 1
        if smer_to['to'] == direction_from:
            if delka == MAX_DELKA:
                continue
            else:
                offset += delka
        
        point_actual_candidate = vypocitej_coord(mapa,point_actual,smer_to['to'])
        if point_actual_candidate: #and \
            #tuple([tuple(point_actual_candidate),tuple(point_from_candidate),offset, ]) not in zasobnik_cache:
            #zasobnik.add(tuple([tuple(point_actual_candidate),tuple(point_from_candidate),offset]))
            vysledek_candidate = walk_it_recursive(mapa,point_actual_candidate,point_from_candidate,offset,hloubka+1,cena_cesty+int(hodnota))
            if not best_vysledek or (vysledek_candidate and best_vysledek>vysledek_candidate):
                best_vysledek = vysledek_candidate
            #walk_cache[tuple([tuple(point_actual_candidate),tuple(point_from_candidate),offset])] = 0
    #print(f"{' '*hloubka} {hloubka}:vracim nejlepsi vysledek pro {point_actual}: {best_vysledek}")
    if best_vysledek:
        return best_vysledek + int(hodnota)
    return None
    #zasobnik_cache.add(tuple([tuple(point_actual),tuple(point_from)]))
def main():
    global walk_cache
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
    start = int(mapa[0][0])
    start_time = time.time()
    vysledek = walk_it_s_while(mapa,[0,0], [0,-1],0)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Vysledek: {vysledek} za {elapsed_time} sekund')
    walk_cache = {}
    global_best = 0
    #vysledek = None
    #vysledek2 = walk_it_recursive(mapa,[0,0], [0,-1],0)
    vysledek2 = vysledek
    print(vysledek-start,vysledek2-start,global_best)
if __name__ == '__main__':
    main()