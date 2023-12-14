import os
import logging
import itertools
import re
import time
import collections
import copy
import sys
import concurrent.futures
from line_profiler import LineProfiler
kyble_cache = {}
def kyble(kyble_fronta:list, pocty_fronta:list,indent=0):
    #kyble_fronta_orig = copy.deepcopy(kyble_fronta)
    #pocty_fronta_orig = copy.deepcopy(pocty_fronta)
    #print('  '*indent + f'Zkousim kyble: {kyble_fronta}, {pocty_fronta}\t{indent}')
    #global kyble_cache
    #klic = ''.join(kyble_fronta) + 'X'+''.join([str(znak) for znak in pocty_fronta])
    #if kyble_cache.get(klic):
    #    return kyble_cache.get(klic)
    if len(pocty_fronta) == 0:
        if ''.join(kyble_fronta).find('#') == -1:
            #print('  '*indent + 'Zvedam hodnotu o 1')
            return 1
        else:
            return 0
    elif not kyble_fronta:
        return 0
        
    ret_value = 0
    pocet = pocty_fronta.pop()
    
    
    while kyble_fronta :
        #print('  '*indent + f'Iteruji({i}) nad kybly {kyble_fronta}, {pocty_fronta}, {pocet}\t{indent}')
        kybl = kyble_fronta.pop()
        
        
        
        while pocet <= len(kybl):
            #kyble_fronta_copy = copy.copy(kyble_fronta)
            kyble_fronta_copy = kyble_fronta.copy()
            #pocty_fronta_copy = copy.copy(pocty_fronta)
            #pocty_fronta_copy = pocty_fronta
            if len(kybl) > pocet+1:
                kyble_fronta_copy.append(kybl[pocet+1:])
            if len(kybl) > pocet and kybl[pocet]!='#' or len(kybl) == pocet:
                #print('  '*indent + f'Volam({pocet},{kybl}), ret_value={ret_value}, {kyble_fronta_copy}, {pocty_fronta_copy} \t{indent}')
                ret_value += kyble(kyble_fronta_copy,pocty_fronta,indent+1)
            if kybl[0] == '#':
                break
            kybl = kybl[1:]
    pocty_fronta.append(pocet)
            
        
    #print('  '*indent + f'ret_value: {ret_value} ({kyble_fronta_orig,pocty_fronta_orig})')
    #kyble_cache[klic] = ret_value
    return ret_value
#def plnici_metoda
def kyblikova_metoda(radka:str, orig:str):
    start_time = time.time()
            
    print('zkousim kyblikova',orig)
    zadani = list(radka.split(' ')[0])
    pocty_fronta = [int(pocet) for pocet in radka.split(' ')[1].split(',')]
    pocty_fronta.reverse()
    zadani_unif = re.sub('[\\.]','_',''.join(zadani))
    kyble_fronta = [k for k in re.sub('(_)\\1+','\\1',zadani_unif).split('_') if k!='']
    kyble_fronta.reverse()
    ret_value = kyble(kyble_fronta,pocty_fronta)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f'Vysledek: {ret_value} za {elapsed_time} sekund')
    return ret_value
def kyblikova_metoda_mp(radka:str):
    nova = rozsir_radek(radka,5)
    return kyblikova_metoda(nova,radka)
    
    




def rozsir_radek(radka:str, extended:int = 1):
    radka = radka.strip()
    zadani_z = radka.split(' ')[0]
    #pocty_z = ','.join([int(pocet) for pocet in radka.split(' ')[1].split(',')])
    pocty_z = radka.split(' ')[1]
    
    zadani = '?'.join([zadani_z for _ in range(extended)])
    pocty = ','.join([pocet for pocet in ','.join([pocty_z for _ in range(extended)]).split(',')])
    return ' '.join([zadani,pocty])

        
    
def zkus_radku(radka: str, extended:int = 1):
    zadani_z = radka.split(' ')[0]
    #pocty_z = ','.join([int(pocet) for pocet in radka.split(' ')[1].split(',')])
    pocty_z = radka.split(' ')[1]
    
    zadani = '?'.join([zadani_z for _ in range(extended)])
    pocty = [int(pocet) for pocet in ','.join([pocty_z for _ in range(extended)]).split(',')]
    pocet_otazniku = zadani.count('?')
    pocty_regularni_vyraz = ''.join(['#{'+ str(pocet) + '}'+'\\.+' for pocet in pocty])[:-3]
    #varianty_regularni_vyraz = ''.join(['#{}' + str(pocet) ])
    pocet_hledanych_rozbitych = sum(pocty) - zadani.count('#')
    logging.debug(f'Resim radku se zadanim {zadani} ({pocet_otazniku} neznamych) a pocty {pocty}. Regularni vyraz: {pocty_regularni_vyraz}')
    vhodne_varianty = [varianta for varianta in itertools.product(['.','#'],repeat=pocet_otazniku) \
        if varianta.count('#') == pocet_hledanych_rozbitych] #and  re.search(varianty_regularni_vyraz,''.join(varianta))
    logging.debug(f'Celkovy pocet kandidatskych variant je: {len(vhodne_varianty)}')
    pocet_variant = 0
    for varianta in vhodne_varianty:
        #logging.debug(f"Zkousim variantu {varianta}")
        pracovni_zadani = zadani
        for znak in varianta:
            pracovni_zadani = pracovni_zadani.replace('?',znak,1)
        
        if re.search(pocty_regularni_vyraz,pracovni_zadani):
            pocet_variant+=1
        
        
    logging.debug(f'Resim radku se zadanim {zadani} ({pocet_otazniku} neznamych) a pocty {pocty}, pocet nalezenych variant = {pocet_variant}')
    return pocet_variant

#kyblikova_metoda('.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##. 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3')
#sys.exit(1)
#kyblikova_metoda(rozsir_radek('?????.#...#... 4,1,1',1))


radka = '???.???#????.???? 1,5,2,1'
#radka = '????.#...#... 4,1,1'

kyblikova_metoda(rozsir_radek(radka,2), radka)
profiler = LineProfiler()
profiler.add_function(kyble)   # add additional function to profile
lp_wrapper = profiler(kyblikova_metoda)
lp_wrapper(rozsir_radek(radka,2), radka)
#profiler.disable()
profiler.print_stats()
#kyblikova_metoda(rozsir_radek('?????????.???..?#?? 7,1,1,3',5))
#sys.exit(1)



def main():
    
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    pocitadlo = 0
    pocitadlo2 = 0
    
    with open(input_file) as f:
        #with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        #    results = list(executor.map(kyblikova_metoda_mp, f.readlines()))
        for line in f.readlines():
            kyblikova_metoda_mp(line)
        
    print(results)
    print(sum(results))
    print(f'Part1: {pocitadlo}')
    print(f'Part2: {pocitadlo2}')
if __name__ == '__main__':
    main()