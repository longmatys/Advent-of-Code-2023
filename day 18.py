import os
import logging
import collections
import sys
import copy
import ordered_set
import itertools
import sortedcontainers 
import alive_progress
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
ZATACKY = {
    'L':{
        'L': {'smer':'rovne','vnejsi':[]},
        'R': {'smer':'rovne','vnejsi':[]},
        'U': {'smer':'R','vnejsi':[mapa_stran['west']['from'],mapa_stran['south']['from']]},
        'D': {'smer':'L','vnejsi':[mapa_stran['west']['from'],mapa_stran['north']['from']]}
    },
    'R':{
        'L': {'smer':'rovne','vnejsi':[]},
        'R': {'smer':'rovne','vnejsi':[]},
        'U': {'smer':'L','vnejsi':[mapa_stran['east']['from'],mapa_stran['south']['from']]},
        'D': {'smer':'R','vnejsi':[mapa_stran['east']['from'],mapa_stran['north']['from']]},
    },
    'U':{
        'L': {'smer':'L','vnejsi':[mapa_stran['north']['from'],mapa_stran['east']['from']]},
        'R': {'smer':'R','vnejsi':[mapa_stran['north']['from'],mapa_stran['west']['from']]},
        'U': {'smer':'rovne','vnejsi':[]},
        'D': {'smer':'rovne','vnejsi':[]},
    },
    'D':{
        'L': {'smer':'R','vnejsi':[mapa_stran['south']['from'],mapa_stran['east']['from']]},
        'R': {'smer':'L','vnejsi':[mapa_stran['south']['from'],mapa_stran['west']['from']]},
        'U': {'smer':'rovne','vnejsi':[]},
        'D': {'smer':'rovne','vnejsi':[]},
    },
}
PART2_MAP = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
    #0 means R, 1 means D, 2 means L, and 3 means U
}
def flood_it(mapa_navstivenosti,smer_zatacky):
    seznam = set()
    for i,line in enumerate(mapa_navstivenosti):
        for j,bod in enumerate(line):
            if bod==smer_zatacky:
                seznam.add((i,j))
    while (len(seznam)):
        point_actual = seznam.pop()
        for smer in mapa_stran.keys():
            new_point = vypocitej_coord(mapa_navstivenosti,point_actual,mapa_stran[smer].get('from'))
            if new_point:
                instrukce = mapa_navstivenosti[new_point[0]][new_point[1]]
                #if instrukce == False and mapa[new_point[0]][new_point[1]]=='.':
                if instrukce == '.':
                    mapa_navstivenosti[new_point[0]][new_point[1]] = smer_zatacky
                    seznam.add((new_point[0],new_point[1]))
def aktualizuj_rohy(rohy, point):
    rohy[0][0] = min(rohy[0][0],point[0])
    rohy[1][0] = max(rohy[1][0],point[0])
    rohy[0][1] = min(rohy[0][1],point[1])
    rohy[1][1] = max(rohy[1][1],point[1])
DECODE_MODE = 'Part2'
def decode_krok(krok,cast_kroku):
    if DECODE_MODE == 'Part1':
        if cast_kroku == 0:
            return krok[0]
        if cast_kroku == 1:
            return int(krok.split(' ')[1])
    else:
        if cast_kroku == 1:
            return int(krok.split('#')[1][:-2],16)
        if cast_kroku == 0:
            return PART2_MAP[krok.split('#')[1][-2]]
            
def aktulizuj_point(point,krok):
    match decode_krok(krok,0):
        case 'R':
            point[1]+=decode_krok(krok,1) 
        case 'L':
            point[1]-=decode_krok(krok,1)             
        case 'D':
            point[0]+=decode_krok(krok,1)             
        case 'U':
            point[0]-=decode_krok(krok,1) 
def vypocitej_coord(mapa,point_from,offset_to):
    new_point =  (point_from[0]+offset_to[0],point_from[1]+offset_to[1])
    if new_point[0] < 0 or new_point[1] < 0 or new_point[0] == len(mapa) or new_point[1] == len(mapa[0]):
        return None
    return new_point       
def najdi_rohy(kroky:list):
    point = [0,0]
    rohy = [[0,0],[0,0]]
    for krok in kroky:
        aktulizuj_point(point,krok)
        aktualizuj_rohy(rohy,point)
    return rohy
def nakresli_znak(mapa,point,znak):
    mapa[point[0]][point[1]] = znak
def aktualizuj_vnejsi_rohy(mapa:list, point:list, pokyn_aktualni:str, pokyn_posledni:str):
    return_val = []
    for pokyn in ZATACKY[pokyn_aktualni[0]][pokyn_posledni[0]]['vnejsi']:
        point_candidate = vypocitej_coord(mapa,point,pokyn)
        if point_candidate:
            if mapa[point_candidate[0]][point_candidate[1]] == '.':
                mapa[point_candidate[0]][point_candidate[1]] = ZATACKY[pokyn_aktualni[0]][pokyn_posledni[0]]['smer']
    return ZATACKY[pokyn_aktualni[0]][pokyn_posledni[0]]['smer']

def nakresli_kroky(mapa:list,kroky:list,start_point):
    point = start_point
    nakresli_znak(mapa,point,'#')
    posledni_krok = kroky[0]
    smerovani = collections.Counter()
    for krok in kroky:
        smerovani.update([aktualizuj_vnejsi_rohy(mapa,point,decode_krok(krok,0),posledni_krok[0])])
        match decode_krok(krok,0):
            case 'R':
                for _ in range(decode_krok(krok,1)):
                    point[1]+=1
                    nakresli_znak(mapa,point,'#')                
            case 'L':
                for _ in range(decode_krok(krok,1)):
                    point[1]-=1
                    nakresli_znak(mapa,point,'#')
            case 'D':
                for _ in range(decode_krok(krok,1)):
                    point[0]+=1
                    nakresli_znak(mapa,point,'#')
            case 'U':
                for _ in range(decode_krok(krok,1)):
                    point[0]-=1
                    nakresli_znak(mapa,point,'#')
        posledni_krok = krok
    return smerovani.most_common(2)[1][0]
def vytvor_sloupce(kroky):
    point = [0,0]
    sloupce = {}
    for krok in kroky:
        match decode_krok(krok,0):
            case 'R':
                point[1]+=decode_krok(krok,1)
                    
            case 'L':
                point[1]-=decode_krok(krok,1)
            case 'D':
                start = point[0]
                point[0]+=decode_krok(krok,1)
                if not sloupce.get(start):
                    sloupce[start] = {}
                sloupce[start][point[1]] = point[0]
            case 'U':
                start = point[0]
                point[0]-=decode_krok(krok,1)
                if not sloupce.get(point[0]):
                    sloupce[point[0]] = {}
                sloupce[point[0]][point[1]] = start
    return sloupce
def spocitej_sloupce(sloupce:dict, pocet_radek):
    zacatek = min(sloupce.keys())
    konec = max(sloupce.keys())
    counter = zacatek
    ret_value = 0
    global DECODE_MODE
    DECODE_MODE = 'Part2'
    #Zasobnik ma v sobe cisla sloupcu 
    
    zasobnik = sortedcontainers.SortedSet()
    zasobnik_cache = {}
    for sloupec in sloupce[counter].keys():
        zasobnik.add(sloupec)
        zasobnik_cache[sloupec] = counter
    with alive_progress.alive_bar(pocet_radek) as bar:

        while zasobnik or counter < konec:
            if counter % 100 == 0:
                bar(100)
            #print(f'Prochazim tento zasobnik: {zasobnik}')
            vnitrek = True
            hrana_counter = 0
            for dvojice in itertools.pairwise(zasobnik):
                #print(f'Zpracovavam {dvojice}')
                #hrana - alespon jeden zacina nebo konci
                
                start_and_start = zasobnik_cache[dvojice[0]] == counter and zasobnik_cache[dvojice[1]] == counter
                end_and_end = sloupce[zasobnik_cache[dvojice[0]]][dvojice[0]] == counter and sloupce[zasobnik_cache[dvojice[1]]][dvojice[1]] == counter
                start_and_end = (sloupce[zasobnik_cache[dvojice[0]]][dvojice[0]] == counter and zasobnik_cache[dvojice[1]] == counter) or \
                    (zasobnik_cache[dvojice[0]] == counter and sloupce[zasobnik_cache[dvojice[1]]][dvojice[1]] == counter)
                if start_and_start or end_and_end or start_and_end:
                    hrana_counter+=1
                else:
                    #Hrany musi jit za sebou, abych si na ne musel davat pozor - zuby _TT_TT_
                    hrana_counter=0
                if vnitrek or (hrana_counter%2 > 0 and (start_and_start  or end_and_end or start_and_end)):
                    ret_value += (dvojice[1] - dvojice[0]) - 1
                else:
                    a=1
                
                
                #Ten druhy nesmi konci, jinak je to hrana a jsem porad stejne
                if  hrana_counter%2 > 0 and start_and_end:
                    "" #Nic nedelam
                else:
                    vnitrek = not vnitrek
                
            #Ty, co konci, tak vyndam a zapoctu jejich vysku
            for sloupec in [sloupec for sloupec in zasobnik if sloupce[zasobnik_cache[sloupec]][sloupec] == counter]:
                zasobnik.discard(sloupec)
                #Prictu vysku odstraneneho sloupce
                ret_value += (sloupce[zasobnik_cache[sloupec]][sloupec] - zasobnik_cache[sloupec])+1
            #na konci zvednu citac a pridam pripadne nove polozky
            counter+=1
            if sloupce.get(counter):
                for sloupec in sloupce[counter].keys():
                    zasobnik.add(sloupec)
                    zasobnik_cache[sloupec] = counter
    return ret_value 
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    kroky = []
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            kroky.append(line)
    if DECODE_MODE == 'Part1' and False:
        rohy = najdi_rohy(kroky)
        print(rohy,rohy[1][0]-rohy[0][0],'x', rohy[1][1]-rohy[0][1],f'Char: {sys.getsizeof(["."])}, Potrebuji: {(rohy[1][0]-rohy[0][0]) * (rohy[1][1]-rohy[0][1]) *sys.getsizeof(["."])/1024/1024/1024} GB pameti')
        mapa = [['.']*(abs(rohy[1][1]-rohy[0][1])+1) for _ in range((abs(rohy[1][0]-rohy[0][0]))+1)]
        
        vnitrni_symbol = nakresli_kroky(mapa,kroky, [-rohy[0][0],-rohy[0][1]])
        
        for line in mapa:
            print(''.join(line))
        flood_it(mapa,vnitrni_symbol)
        pocet = sum([line.count(vnitrni_symbol) for line in mapa])
        pocet += sum([line.count('#') for line in mapa])
        print(f'Pocet vykopanych mist: {pocet}')
        counter = 0
        for i,line in enumerate(mapa):
            counter += line.count(vnitrni_symbol) + line.count("#")
            print(f'{i}:{counter}')
            
    else:
        rohy = najdi_rohy(kroky)
        print('Jdu vytvorit sloupce')
        sloupce = vytvor_sloupce(kroky)
        print('Jdu spocitat vnitrni prostory')
        pocet = spocitej_sloupce(sloupce,rohy[1][0]-rohy[0][0])
        print(pocet)
if __name__ == '__main__':
    main()