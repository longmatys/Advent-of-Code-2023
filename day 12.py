import os
import logging
import itertools
import re
import time
import collections
import copy
def kyble(kyble_fronta:collections.deque, pocty_fronta:collections.deque,indent=0):
    kyble_fronta_orig = copy.deepcopy(kyble_fronta)
    pocty_fronta_orig = copy.deepcopy(pocty_fronta)
    print('  '*indent + f'Zkousim kyble: {kyble_fronta}, {pocty_fronta}\t{indent}')
    if len(pocty_fronta) == 0:
        if ''.join(kyble_fronta).find('#') == -1:
            print('  '*indent + 'Zvedam hodnotu o 1')
            return 1
        else:
            return 0
    elif len(kyble_fronta) == 0:
        return 0
        
    ret_value = 0
    
    kybl = kyble_fronta.popleft()
    pocet = pocty_fronta.popleft()
    i = 0
    while i+pocet <= len(kybl):
    #for i in range( len(kybl) - pocet + 1):
        #    #?????#?###?#???
        #    5
        #    #????. - #?###?#???
        #Try it with spending pocet
        #if len(kybl) + i == pocet:
        #    #do konce uz zbyva jen same #
        #    print('  '*indent + f'Volam 1, ret_value={ret_value} \t{indent}')
        #    ret_value+=kyble(copy.deepcopy(kyble_fronta),copy.deepcopy(pocty_fronta),indent+1)
        if len(kybl)!=i+pocet and kybl[pocet+i-1+1] == '#':
                #neplatna varianta - musim doplnit tecku, ale je tam #
                ""
        elif len(kybl) + i + 1 == pocet:
            #je tam jenom o jedna vic, ale jenom prostor na tecku
            #nemusim nic upravovat
            ""
        else:
            kybl_rest = kybl[pocet+i+1:]
            kyble_fronta_copy = copy.deepcopy(kyble_fronta)
            if kybl_rest != '':
                kyble_fronta_copy.appendleft(kybl_rest)
            print('  '*indent + f'Volam 2, ret_value={ret_value} \t{indent}')
            ret_value += kyble(kyble_fronta_copy,copy.deepcopy(pocty_fronta),indent+1)
            
        #Try it without spending pocet
        if kybl[0] == '#':
            #neplatna varianta, musim to pouzit
            ""
            return ret_value
        else:
            kybl_rest = kybl[1:]
            kyble_fronta_copy = copy.deepcopy(kyble_fronta)
            if kybl_rest != '':
                kyble_fronta_copy.appendleft(kybl_rest)
            pocty_fronta_copy = copy.deepcopy(pocty_fronta)
            pocty_fronta_copy.appendleft(pocet)
            print('  '*indent + f'Volam 3, ret_value={ret_value} \t{indent}')
            ret_value += kyble(kyble_fronta_copy,pocty_fronta_copy,indent+1)
                
        i+=1
    print('  '*indent + f'ret_value: {ret_value} ({kyble_fronta_orig,pocty_fronta_orig})')
    return ret_value
def kyblikova_metoda(radka:str):
    print('zkousim kyblikova',radka)
    zadani = list(radka.split(' ')[0])
    pocty_fronta = collections.deque([int(pocet) for pocet in radka.split(' ')[1].split(',')])
    zadani_unif = re.sub('[\\.]','_',''.join(zadani))
    kyble_fronta = collections.deque([k for k in re.sub('(_)\\1+','\\1',zadani_unif).split('_') if k!=''])
    ret_value = kyble(kyble_fronta,pocty_fronta)
    print(ret_value)
def optimalizuj_retez_uprostred(radka:str):
    print('zkousim optimalizovat uprostred',radka)
    zadani = list(radka.split(' ')[0])
    pocty = collections.deque([int(pocet) for pocet in radka.split(' ')[1].split(',')])
    
    result_parts = []
    result_pocty = []
    b = re.sub('(\\.)\\1+','\\1',''.join(zadani)).split('.')
    
    zadani_unif = re.sub('[?\\.]','_',''.join(zadani))
    zadani_uniq = re.sub('(.)\1+','\1',zadani_unif)
    zadani_a = [vnitrek for vnitrek in zadani_uniq.split('_') if vnitrek!='']
    if len(zadani_a) == len(pocty):
        print(zadani)
    
    
def optimalizuj_retez_zprava(radka:str):
    print('zkousim optimalizovat zprava',radka)
    zadani = list(radka.split(' ')[0])
    pocty = collections.deque([int(pocet) for pocet in radka.split(' ')[1].split(',')])
    
    result_parts = []
    result_pocty = []
    #nejdriv zkusim oriznout zprava zbytecne otazniky
    
    while True:
        regex = '(.*[^?#]+)([?#]{1,' + str(pocty[-1]-1) + '})(\\.*)$'
        vstup = ''.join(zadani)
        b = re.sub(regex,'\\1|\\2|\\3',vstup)
        if b == ''.join(zadani):
            break
    """
    while True:
        #regex = '^([\\.]*)[#?]{' + str(pocty[0]) + '}[\\.?](.*)'
        regex = '(.*)[\\.?][#?]{' + str(pocty[0]) + '}([\\.]*)$'
        b = re.sub(regex,'\\1|' +'#'*pocty[-1] + '.\\2',''.join(zadani))
        if b == ''.join(zadani):
            break
        else:
            result_parts.append(b.split('|')[0])
            zadani = list(b.split('|')[1])
            result_pocty.append(pocty.popleft())
    """
    return ''.join(zadani) + ' ' + ','.join([str(cislo) for cislo in pocty])

#optimalizuj_retez_zprava('?..?.#????#?###?#? 1,1,1,10')
#optimalizuj_retez_uprostred('????#?#???..??? 1,3')

def optimalizuj_retez_zleva(radka:str):
    print('zkousim optimalizovat',radka)
    zadani = list(radka.split(' ')[0])
    pocty = collections.deque([int(pocet) for pocet in radka.split(' ')[1].split(',')])
    
    result_parts = []
    result_pocty = []
    
    while True:
        regex = '^([\\.]*#)[#?]{' + str(pocty[0]-1) + '}[\\.?](.*)'
        b = re.sub(regex,'\\1' +'#'*pocty[0] + '.|\\2',''.join(zadani))
        if b == ''.join(zadani):
            break
        else:
            result_parts.append(b.split('|')[0])
            zadani = list(b.split('|')[1])
            result_pocty.append(pocty.popleft())
    vysledek =  ''.join(result_parts) + ''.join(zadani) + ' ' + ','.join([str(cislo) for cislo in result_pocty + list(pocty)])
    return vysledek

def rozsir_radek(radka:str, extended:int = 1):
    zadani_z = radka.split(' ')[0]
    #pocty_z = ','.join([int(pocet) for pocet in radka.split(' ')[1].split(',')])
    pocty_z = radka.split(' ')[1]
    
    zadani = '?'.join([zadani_z for _ in range(extended)])
    pocty = ','.join([pocet for pocet in ','.join([pocty_z for _ in range(extended)]).split(',')])
    return ' '.join([zadani,pocty])
def zkus_radku_metoda2(radka: str, pattern = None):
    zadani = radka.split(' ')[0]
    pocty = [int(pocet) for pocet in radka.split(' ')[1].split(',')]
    
    
    
    pocet_otazniku = zadani.count('?')
    if not pattern:
        pattern  = re.compile('\\.*' + ''.join(['[#?]{'+ str(pocet) + '}'+'[\\.?]+' for pocet in pocty])[:-6] + '[^#]*$')
    v = pattern.match(zadani)
    if not v:
        return 0
    if pocet_otazniku == 0:
        #logging.debug(f'Nasel jsem reseni pro radku se zadanim {zadani} ({pocet_otazniku} neznamych) a pocty {pocty}. Regularni vyraz: {pocty_regularni_vyraz}')
        return 1
    
    
    
    
    leva = zkus_radku_metoda2(radka.replace('?','.',1),pattern)
    prava = zkus_radku_metoda2(radka.replace('?','#',1),pattern)
    return  leva +  prava
    

        
        
    
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

#kyblikova_metoda(rozsir_radek('???.### 1,1,3',5))
kyblikova_metoda(rozsir_radek('?????.#...#... 4,1,1',1))
kyblikova_metoda(rozsir_radek('????.#...#... 4,1,1',5))



def main():
    
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    pocitadlo = 0
    pocitadlo2 = 0
    
    with open(input_file) as f:
        for i,line in enumerate(f.readlines()):
            line = line.strip()
            if line == '#':
                break
            logging.debug(line)
            pocitadlo += zkus_radku_metoda2(line)
            start_time = time.time()
            pocitadlo2 += zkus_radku_metoda2(optimalizuj_retez_zleva(rozsir_radek(line,5)))
            #pocitadlo2 += zkus_radku_metoda2(rozsir_radek(line,5))
            end_time = time.time()
            elapsed_time = end_time - start_time
            logging.debug(f'Zkusil jsem zadani {i+1}:{line} a pocitadla jsou ({pocitadlo}/{pocitadlo2}). Ubehlo {elapsed_time}s')
    print(f'Part1: {pocitadlo}')
    print(f'Part2: {pocitadlo2}')
if __name__ == '__main__':
    main()