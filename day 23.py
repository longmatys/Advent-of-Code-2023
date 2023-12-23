import os
import logging
import sys
sys.setrecursionlimit(2500)
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
def update_zkratky(zkratky,krizovatka_start,smer_start,new_point,smer_from_new_point,zkratka_delka):
    if not zkratky.get(krizovatka_start):
        zkratky[krizovatka_start] = {}
    zkratky[krizovatka_start][smer_start] = [new_point,zkratka_delka]
    if not zkratky.get(new_point):
        zkratky[new_point] = {}
    zkratky[new_point][smer_from_new_point] = [krizovatka_start,zkratka_delka]
def ziskej_zkratku(zkratky,point_actual,smer):
    if zkratky.get(point_actual) and zkratky[point_actual].get(smer):
        return zkratky[point_actual][smer]
    return None

        
def walk_it_recursive(mapa:list,point_actual:tuple,point_cil:tuple, krizovatky=[]):
    best_delka_cesty = None
    zkratky = {}
    varianty = []
    varianty.append([point_actual,0,[point_actual],point_actual,0])
    
    
    while varianty:
        (point_actual,delka_cesty, historie,krizovatka_start, krizovatka_start_delka) = varianty.pop()
        
        instrukce = mapa[point_actual[0]][point_actual[1]]
        if instrukce == '#':
            continue
        if point_actual == point_cil:
            print(f'Nasel jsem cil: {delka_cesty}, {len(historie)}, {len(varianty)}')
            if best_delka_cesty is None or delka_cesty > best_delka_cesty:
                print(f'Nasel jsem docasne nejdelsi cestu: {delka_cesty}')   
                for a in historie:
                    print(a)
                return 0
                best_delka_cesty = delka_cesty
            continue
        instrukce = '.'
        for smer in mapa_instrukci[instrukce]:
            zkratka = ziskej_zkratku(zkratky,point_actual,smer)
            if not zkratka:
                new_point = vypocitej_coord(mapa,point_actual,smer)
                if new_point:
                    if new_point not in historie and mapa[new_point[0]][new_point[1]] != '#':
                        if new_point in krizovatky:
                            update_krizovatky(krizovatky,smer,krizovatka_start,new_point,krizovatka_start_delka)
                        varianty.append([new_point,delka_cesty+1,list(historie)+[point_actual]])
                    
        
    return best_delka_cesty
def najdi_krizovatky(mapa:list):
    krizovatky = []
    for x,line in enumerate(mapa):
        for (y,pozice) in enumerate(line):
            pocitadlo = 0
            if pozice == '#':
                continue
            for smer in mapa_instrukci['.']:
                new_point = vypocitej_coord(mapa,(x,y),smer)
                if new_point and mapa[new_point[0]][new_point[1]]!='#':
                    pocitadlo+=1
            if pocitadlo > 2:
                krizovatky.append((x,y))
    krizovatky.append(tuple([0,mapa[0].find('.')])) #start
    krizovatky.append(tuple([len(mapa)-1,mapa[-1].find('.')]))   #konec
    return krizovatky
def walk_it(mapa:list,historie:set,point_actual:tuple,point_cile:list):
    step_counter = 0
    smery = []
    
    
    historie.add(point_actual)
    instrukce = mapa[point_actual[0]][point_actual[1]]
    if instrukce == '#':
        historie.remove(point_actual)
        return None
    if point_actual in point_cile:
        historie.remove(point_actual)
        return [0,point_actual,None]
    ret_value = None
    for smer in mapa_instrukci[instrukce]:
        new_point = vypocitej_coord(mapa,point_actual,smer)
        if new_point:
            if new_point not in historie and mapa[new_point[0]][new_point[1]] != '#':
                #bod je platny, jsem stale uvnitr mapy
                vysledek = walk_it(mapa,historie,new_point,point_cile)
                if vysledek is not None and (ret_value is None or vysledek[0] > ret_value[0]):
                    ret_value = vysledek
                    if ret_value[2] is None:
                        ret_value[2] = (-1*smer[0],-1*smer[1])
                    
            else:
                #historie.remove(point_actual)
                continue
    historie.remove(point_actual)
    if ret_value is None:
        return None
    
    return [ret_value[0] + 1, ret_value[1], ret_value[2]]
def walk_zkratky(mapa:list,krizovatky:list):
    zkratky = {}
    for krizovatka in krizovatky:
        point_actual = krizovatka
        
        for smer in mapa_instrukci['.']:
            if not ziskej_zkratku(zkratky,point_actual,smer):
                new_point = vypocitej_coord(mapa,point_actual,smer)
                if new_point and mapa[new_point[0]][new_point[1]] != '#':
                    (start_delka, point_konec, smer_konec) = walk_it(mapa,set(),new_point,krizovatky)
                    update_zkratky(zkratky,krizovatka,smer,point_konec,smer_konec,start_delka+1)
    return zkratky
def najdi_cestu(zkratky,point_start,point_cil):
    best_delka_cesty = None
    
    varianty = []
    varianty.append([point_start,0,[]])
    
    
    while varianty:
        (point_actual,delka_cesty, historie) = varianty.pop()
        if point_actual in historie:
            continue
        if point_actual == point_cil:
            #print(f'Nasel jsem cil: {delka_cesty}, {len(historie)}, {len(varianty)}')
            if best_delka_cesty is None or delka_cesty > best_delka_cesty:
                print(f'Nasel jsem docasne nejdelsi cestu: {delka_cesty}')   
                #for a in historie:
                #    print(a)
                #return 0
                best_delka_cesty = delka_cesty
            continue
        
        for (smer_zkratka,cil_zkratka) in zkratky[point_actual].items():
            
            varianty.append([cil_zkratka[0],delka_cesty+cil_zkratka[1],list(historie)+[point_actual]])
                    
        
    return best_delka_cesty
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
    vysledek = walk_it(mapa,set(),tuple([0,mapa[0].find('.')]),[tuple([len(mapa)-1,mapa[-1].find('.')])])
    print(vysledek)
    krizovatky = najdi_krizovatky(mapa)
    #vysledek2 = walk_it_recursive(mapa,tuple([0,mapa[0].find('.')]),tuple([len(mapa)-1,mapa[-1].find('.')]),krizovatky)
    #print(vysledek2)
    zkratky = walk_zkratky(mapa,krizovatky)
    print(krizovatky, len(krizovatky))
    vysledek = najdi_cestu(zkratky,tuple([0,mapa[0].find('.')]),tuple([len(mapa)-1,mapa[-1].find('.')]))
    print(vysledek)
if __name__ == '__main__':
    main()