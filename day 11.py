import os
import logging
import collections
import itertools
def expand_universe_lines_usporne(mapa_puvodni):
    prazdne = []
    for i,line in enumerate(mapa_puvodni):
        pocitej = collections.Counter(line)
        
        if len(pocitej.keys())== 1 and line[0]== '.':
            prazdne.append(i)
            
    return prazdne
def expand_universe_usporne(mapa):
    radky = expand_universe_lines_usporne(mapa)
    
    mapa = list(zip(*mapa))
    sloupce = expand_universe_lines_usporne(mapa)
    #Transpose back
    return (radky,sloupce)
def najdi_galaxie(mapa):
    indexes = []
    for i,line in enumerate(mapa):
        indexes += [(i,index) for index, value in enumerate(line) if value == '#']
    return indexes
def tiskni_mapu(mapa):
    for line in mapa:
        logging.debug(line)

def vzdalenost_usporne(dvojice,vsechny_expanze, expanze_size):
    min_row = min(dvojice[0][0],dvojice[1][0])
    max_row = max(dvojice[0][0],dvojice[1][0])
    min_column = min(dvojice[0][1],dvojice[1][1])
    max_column = max(dvojice[0][1],dvojice[1][1])
    expanze_row = [expanze for expanze in vsechny_expanze[0] if expanze>min_row and expanze < max_row]
    expanze_column = [expanze for expanze in vsechny_expanze[1] if expanze>min_column and expanze < max_column]
    
    return abs(dvojice[0][0]-dvojice[1][0]) + abs(dvojice[0][1]-dvojice[1][1]) + (expanze_size-1)*(len(expanze_row)+len(expanze_column))
    
def spocitej_vzalenosti(vsechny_galaxie):
    ret_value = []
    for dvojice in itertools.combinations(vsechny_galaxie,2):
        ret_value += [vzdalenost(dvojice)]
    return ret_value
def spocitej_vzalenosti_usporne(vsechny_galaxie,expanze, expanze_size=1000000):
    ret_value = []
    for dvojice in itertools.combinations(vsechny_galaxie,2):
        ret_value += [vzdalenost_usporne(dvojice,expanze,expanze_size)]
    return ret_value
def main():
    mapa_puvodni = []
# Get the name of the Python script
    logging.basicConfig(level=logging.INFO, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '#':
                break
            mapa_puvodni.append(line)
            logging.debug(line)
    
    #mapa = expand_universe(mapa_puvodni)
    vsechny_galaxie = najdi_galaxie(mapa_puvodni)
    vsechny_expanze = expand_universe_usporne(mapa_puvodni)
    vzdalenosti1 = spocitej_vzalenosti_usporne(vsechny_galaxie,vsechny_expanze,2)
    vzdalenosti2 = spocitej_vzalenosti_usporne(vsechny_galaxie,vsechny_expanze)
    print(f'Part 1: {sum(vzdalenosti1)}, Part 2: {sum(vzdalenosti2)}')
    
if __name__ == '__main__':
    main()