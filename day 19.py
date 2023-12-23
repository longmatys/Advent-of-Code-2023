import os
import logging
import json
import copy
import itertools
MAX_RANGE = 4000
MIN_RANGE = 1
def je_mensi(op1,op2,cil):
    if op1 is None:
        return (cil,range(1,int(op2)),range(int(op2),MAX_RANGE+1))
    if op1 is None or int(op1) < int(op2):
        return (cil,None,None)
    return (None,None,None)
def je_vetsi(op1,op2,cil):
    if op1 is None:
        return (cil,range(int(op2)+1,MAX_RANGE+1),range(1,int(op2)))
    if op1 is None or int(op1) > int(op2):
        return (cil,None,None)
    return (None,None,None)
def skok(op1,op2,cil):
    return (cil,range(MIN_RANGE,MAX_RANGE+1),range(MIN_RANGE,MAX_RANGE+1))

def vyhodnot_prunik(soucastka,parametr,varianta,rozsah):
    soucastka[parametr] = soucastka[parametr] & set(rozsah)
    
def invertuj_ano_ne(soucastka):
    ret_value ={}
    for k,v in soucastka.items():
        ret_value[k] = {'ano': v['ne'], 'ne': v['ano']}
        if v['ne']:
            ret_value[k]['ano'] = range(MIN_RANGE,MAX_RANGE+1)
    return ret_value
class moje_set(set):
    def __str__(self):
        return f"{min(self)}-{max(self)}"
class moje_dict(dict):
    def __str__(self):
        # Customize the string representation for the entire dictionary
        items_str = ', '.join(f"{key}: {moje_set(value).__str__()}" for key, value in self.items())
        return f"{{{items_str}}}"
def moje_print(retez,objekt):
    print(retez, ' ',end='')
    for line in objekt:
        print(moje_dict(line),', ',end='')
    print('')
def vyhodnot_frontu_rozsahy(fronta,fronty,soucastka,indent=0):
    print(' '*indent,f'{indent}. Prochazim: {fronta} {fronty[fronta]}. Vstup:{soucastka}')
    ret_value = []
    for krok in fronty[fronta]:
        print(' '*indent,f'{indent}. Pokousim {krok}')
        [vysledek,rozsah_ano,rozsah_ne] = globals()[krok[0]](None,krok[2],krok[3])
        if vysledek in ['A','R']:
            if vysledek == 'R':
                if krok[1] == '':
                    break
                    return ret_value
            elif vysledek == 'A':
                if krok[1] == '':
                    ret_value.append(soucastka)
                    break
                    return ret_value
                else:
                    soucastka_mistni = moje_dict(soucastka)
                    soucastka_mistni[krok[1]] = soucastka_mistni[krok[1]] & moje_set(rozsah_ano)
                    ret_value.append(soucastka_mistni)
        else:
            soucastka_mistni = moje_dict(soucastka)
            if krok[1] != '':
                soucastka_mistni[krok[1]] = soucastka_mistni[krok[1]] & moje_set(rozsah_ano)
            vysledky_mistni = vyhodnot_frontu_rozsahy(vysledek,fronty,soucastka_mistni,indent+1)
            ret_value+=vysledky_mistni
        if krok[1] != '':
            soucastka[krok[1]] =  soucastka[krok[1]] & set(rozsah_ne)
    moje_print(' '*indent + f'{indent}. Vysledek',ret_value)
    return ret_value
        
    



def vyhodnot_frontu(soucastka,fronta,fronty):
    for krok in fronty[fronta]:
        #print(f'Pokousim {soucastka} {fronta} {fronty[fronta]}')
        atribut = krok[1]
        [vysledek,_,_] = globals()[krok[0]](soucastka.get(krok[1]),krok[2],krok[3])
        if not vysledek:
            continue
        if vysledek in ['A','R']:
            return vysledek
        return vyhodnot_frontu(soucastka,vysledek,fronty)
    return 'NIKDY SE SEM NEDOSTANES'
def projdi_soucastky(soucastky:list, fronty:dict):
    ret_value = 0
    for soucastka in soucastky:
        vysledek =vyhodnot_frontu(soucastka,'in',fronty)
        if vysledek == 'A':
            #print(f'Soucastka {soucastka} byla schvalena')
            ret_value += sum([int(v) for k,v in soucastka.items()])
        else:
            print(f'Soucastka {soucastka} NEBYLA schvalena')
    return ret_value
def analyzuj_vysledky(vysledky):
    total_vysledky = {}
    hranice = {}
    rozsahy_db = {
        'x':{},'m':{},'a':{},'s':{}
    }
    for znak in 'xmas':
        mnozina = set()
        for vysledek in vysledky:
            mnozina.add(min(vysledek[znak]))
            mnozina.add(max(vysledek[znak]))
        hranice[znak] = {'hranice':mnozina,'rozsahy':[]}
        for par in itertools.pairwise(sorted(mnozina)):
            if len(hranice[znak]['rozsahy'])>0:
                rozdil = 1
            else:
                rozdil = 0
            hranice[znak]['rozsahy'].append([f'{par[0]+rozdil}-{par[1]}',set(range(par[0]+rozdil,par[1]+1))])
            rozsahy_db[znak][f'{par[0]+rozdil}-{par[1]}'] = set(range(par[0]+rozdil,par[1]+1))
    for vysledek in vysledky:
        hranice_rozsahy = {}
        
        for znak in 'xmas':
            hranice_rozsahy[znak] = []    
            for znak_rozsah in hranice[znak]['rozsahy']:
                if vysledek[znak] & znak_rozsah[1]:
                    hranice_rozsahy[znak].append(znak_rozsah[0])
        
        for meze_x in hranice_rozsahy['x']:
            for meze_m in hranice_rozsahy['m']:
                for meze_a in hranice_rozsahy['a']:
                    for meze_s in hranice_rozsahy['s']:
                        if not total_vysledky.get(meze_x):
                           total_vysledky[meze_x] = {}
                        if not total_vysledky[meze_x].get(meze_m):
                           total_vysledky[meze_x][meze_m] = {}
                        if not total_vysledky[meze_x][meze_m].get(meze_a):
                           total_vysledky[meze_x][meze_m][meze_a] = {}
                        total_vysledky[meze_x][meze_m][meze_a][meze_s] = True
        
    global_result = 0
    for meze_x, data_x in total_vysledky.items():
        for meze_m, data_m in data_x.items():
            for meze_a, data_a in data_m.items():
                for meze_s in data_a.keys():
                    global_result += len(rozsahy_db['x'][meze_x]) * len(rozsahy_db['m'][meze_m]) * len(rozsahy_db['a'][meze_a]) * len(rozsahy_db['s'][meze_s])
    print(global_result)
def projdi_soucastky_rozsahy(fronty:dict):
    ret_value = 0
    soucastka=moje_dict({
        'x': moje_set(range(MIN_RANGE,MAX_RANGE+1)),
        'm': moje_set(range(MIN_RANGE,MAX_RANGE+1)),
        'a': moje_set(range(MIN_RANGE,MAX_RANGE+1)),
        's': moje_set(range(MIN_RANGE,MAX_RANGE+1)),
    })
    
    vysledky =vyhodnot_frontu_rozsahy('in',fronty,soucastka)
    for vysledek in vysledky:
        docasny_vysledek = 1
        for znak in 'xmas':
            docasny_vysledek = docasny_vysledek * (len(vysledek[znak]))
        #print(f'Vysledek pro {vysledek} je {znak}:{len(vysledek[znak])} {docasny_vysledek}')
        print(f'Vysledek je {vysledek}')
        ret_value+= docasny_vysledek
    analyzuj_vysledky(vysledky)
    return ret_value
    for definice in vysledky:
        for x in [min(definice['x']),max(definice['x'])]:
            for m in [min(definice['m']),max(definice['m'])]:
                for a in [min(definice['a']),max(definice['a'])]:
                    for s in [min(definice['s']),max(definice['s'])]:
                        print('{'+f'x={x},m={m},a={a},s={s}' +'}')
        print(' ')
        
    return ret_value
            
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    zadani_soucastky = False
    soucastky = []
    fronty = {}
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '':
                zadani_soucastky = True
                continue
            if zadani_soucastky:
                soucastka = {}
                for atribut in line[1:-1].split(','):
                    (jmeno,hodnota) = atribut.split('=')
                    soucastka[jmeno]=hodnota
                soucastky.append(soucastka)
            else:
                
                jmeno_fronty = line[0:line.find('{')]
                fronty[jmeno_fronty] = []
                for podminka in line[line.find('{')+1:line.find('}')].split(','):
                    if '<' in podminka:
                        jmeno = podminka[0]
                        operace = 'je_mensi'
                        cislo = podminka[2:podminka.find(':')]
                        vysledek = podminka[podminka.find(':')+1:]
                    elif '>' in podminka:
                        jmeno = podminka[0]
                        operace = 'je_vetsi'
                        cislo = podminka[2:podminka.find(':')]
                        vysledek = podminka[podminka.find(':')+1:]
                    else:
                        jmeno = ''
                        operace = 'skok'
                        cislo = ''
                        vysledek = podminka
                    fronty[jmeno_fronty].append(tuple([operace,jmeno,cislo,vysledek]))
                
                        
    #print(soucastky)
    #print(fronty)
    vysledek = projdi_soucastky(soucastky, fronty)
    print(vysledek)
    vysledek2 = projdi_soucastky_rozsahy(fronty)
    print(f'Vysledek je {vysledek2}')
    
if __name__ == '__main__':
    main()