import os
import logging
import dataclasses
from typing import List, Dict, Type
import collections
PULZ_HIGH = True
PULZ_LOW = False
STAV_ON = True
STAV_OFF = False
DEBUG = False
@dataclasses.dataclass
class class_module:
    vstupy: dict = dataclasses.field(default_factory=dict)
    vystupy: list = dataclasses.field(default_factory=list)
    jmeno: str = ''
    pocitadlo: collections.Counter = dataclasses.field(default_factory=collections.Counter)
    pocitadlo_vystup: collections.Counter = dataclasses.field(default_factory=collections.Counter)
    mozny_vystup: int = 0
    hodiny: int = 0
    konflikty: list = dataclasses.field(default_factory=list)
    def proved_vystup(self, hodiny):
        return []
    def zaregistruj_vstup(self, vstupni_modul):
        self.vstupy[vstupni_modul.jmeno] = vstupni_modul
    def zaregistruj_vystup(self, vystupni_modul):
        self.vystupy.append(vystupni_modul)
        vystupni_modul.zaregistruj_vstup(self)
    def prijmi_vstup(self,vstup,zdroj,hodiny):
        if DEBUG:
            print(f' {self.jmeno} ({self.__class__.__name__}): Prijimam vstup {vstup} od {zdroj}')
        self.hodiny = hodiny        
        self.pocitadlo.update([vstup])
        return True
@dataclasses.dataclass
class broadcaster(class_module):
    posledni_pulz:bool = PULZ_LOW
    def proved_vystup(self, hodiny):
        ret_value = []
        if self.mozny_vystup > 0:
            for vystup in self.vystupy:
                if DEBUG:
                    print(f'  Odesilam {self.jmeno} ({self.__class__.__name__}) {self.posledni_pulz}-> {vystup.jmeno} ({vystup.__class__.__name__}) ')
                self.pocitadlo_vystup.update([f'{vystup.jmeno}_{self.posledni_pulz}'])
                ret_value.append([vystup,self.posledni_pulz,self.jmeno])        
        self.mozny_vystup = 0
        return ret_value
        
    def prijmi_vstup(self, vstup, zdroj, hodiny):
        if super().prijmi_vstup(vstup, zdroj, hodiny):
            self.posledni_pulz = vstup
            self.mozny_vystup = self.hodiny
            return True
        return False
        
@dataclasses.dataclass
class flip_flop(class_module):
    stav:bool = STAV_OFF
    posledni_pulz:bool = PULZ_LOW
    zdroj: str = ''
    
    def proved_vystup(self, hodiny):
        
        ret_value = []
        if self.mozny_vystup > 0:
            for vystup in self.vystupy:
                if DEBUG:
                    print(f'  Odesilam {self.jmeno} ({self.__class__.__name__}) {self.stav}-> {vystup.jmeno}  ({vystup.__class__.__name__})')
                #vystup.prijmi_vstup(self.stav, self.jmeno, hodiny)
                self.pocitadlo_vystup.update([f'{vystup.jmeno}_{self.stav}'])
                ret_value.append([vystup,self.stav,self.jmeno])
        
        self.mozny_vystup = 0
        return ret_value
        
    def prijmi_vstup(self, vstup, zdroj, hodiny):
        if super().prijmi_vstup(vstup, zdroj, hodiny):
            self.zdroj = zdroj
            self.posledni_pulz = vstup
            if vstup == PULZ_LOW:
                self.stav = not self.stav
                self.mozny_vystup = self.hodiny
        
    
@dataclasses.dataclass
class conjunction(class_module):
    vstupy_stav: dict = dataclasses.field(default_factory=dict)
    def zaregistruj_vstup(self, vstupni_modul):
        super().zaregistruj_vstup(vstupni_modul)
        self.vstupy_stav[vstupni_modul.jmeno] = PULZ_LOW
    def proved_vystup(self, hodiny):
        ret_value = []
        if self.mozny_vystup > 0:
            odchozi_signal = PULZ_LOW
            for vstup_stav in self.vstupy_stav.values():
                if vstup_stav == PULZ_LOW:
                    odchozi_signal = PULZ_HIGH
            
            for vystup in self.vystupy:
                if DEBUG:
                    print(f'  Odesilam  {self.jmeno} ({self.__class__.__name__}) {odchozi_signal}-> {vystup.jmeno} ({vystup.__class__.__name__}). {self.vstupy_stav}')
                self.pocitadlo_vystup.update([f'{vystup.jmeno}_{odchozi_signal}'])
                ret_value.append([vystup,odchozi_signal,self.jmeno])
                
        
        self.mozny_vystup = 0
        return ret_value
    def prijmi_vstup(self, vstup, zdroj, hodiny):
        #print('Prijimam vstup')
        if super().prijmi_vstup(vstup, zdroj, hodiny):
            self.vstupy_stav[zdroj] = vstup
            self.mozny_vystup = self.hodiny
        

def propoj_moduly(inventar_modulu:dict, zasobnik_instrukci:list, inventar_modulu_simple:dict):
    
    for instrukce in zasobnik_instrukci:
        [vstup,vystupy] = instrukce.split(' -> ')
        vstup_druh = vstup[0]
        if vstup[0] in ['&','%']:
            vstup = vstup[1:]
        for vystup in vystupy.split(','):
            if not inventar_modulu_simple.get(vystup.strip()):
                inventar_modulu_simple[vystup.strip()] = {'druh': '-', 'vstupy':{}, 'vystup': None, 'vystupy':[], 'vstup':[]}
            if not inventar_modulu.get(vystup.strip()):
                inventar_modulu[vystup.strip()] = class_module(jmeno=vystup.strip())
            inventar_modulu_simple[vstup.strip()]['vystupy'].append(vystup.strip())
            inventar_modulu_simple[vystup.strip()]['vstupy'] = []
            inventar_modulu[vstup.strip()].zaregistruj_vystup(inventar_modulu[vystup.strip()])
            if inventar_modulu_simple[vystup.strip()]['druh'] == '&':
                inventar_modulu_simple[vystup.strip()]['stav'][vstup.strip()] = PULZ_LOW
            inventar_modulu_simple[vystup.strip()]['vstup'].append(vstup.strip())
    #print(inventar_modulu)
def dump_hodiny(inventar_modulu:dict):
    for k,v in inventar_modulu.items():
        print(f'{k} -> {v.mozny_vystup},',end='')
    print("")
def stiskni_tlacitko_simple(inventar_modulu_simple:dict):
    
    pocitadlo_vstup = collections.Counter()
    pocitadlo_vystup = collections.Counter()
    #inventar_modulu['broadcaster'].prijmi_vstup(PULZ_LOW,'tlacitko', hodiny)
    inventar_modulu_simple['broadcaster']['vstupy'].append(('tlacitko', PULZ_LOW))
    fronta = collections.deque()
    fronta.append(('tlacitko','broadcaster',PULZ_LOW))
    
    
    #Nejdriv zpracuji vstupy
    while fronta:
        (vstup_jmeno,cil_jmeno,stav) = fronta.popleft()
        if DEBUG:
            print('\nZacina dalsi runda')    
        vstup_data = inventar_modulu_simple[cil_jmeno]
        if DEBUG:
            print(f'{vstup_jmeno} -{stav}->{cil_jmeno}')
        if inventar_modulu_simple[cil_jmeno]['druh'] == '&':
            inventar_modulu_simple[cil_jmeno]['stav'][vstup_jmeno] = stav
            result = all([l_stav for _,l_stav in vstup_data['stav'].items()])
            for vystup in inventar_modulu_simple[cil_jmeno]['vystupy']:
                fronta.append((cil_jmeno,vystup,not result))
        elif vstup_data['druh'] == '%':
            if stav == PULZ_LOW:
                vstup_data['stav'] = not vstup_data['stav']
                for vystup in inventar_modulu_simple[cil_jmeno]['vystupy']:
                    fronta.append((cil_jmeno,vystup,vstup_data['stav']))
        elif vstup_data['druh'] == 'broadcaster':
            for vystup in inventar_modulu_simple[cil_jmeno]['vystupy']:
                    fronta.append((cil_jmeno,vystup,stav))
        pocitadlo_vystup.update([stav])
        
        
            
    
    return (pocitadlo_vstup, pocitadlo_vystup)
def stiskni_tlacitko(inventar_modulu:dict, hodiny):
    #inventar_modulu['broadcaster'].prijmi_vstup(PULZ_LOW,'tlacitko', hodiny)
    pokracovat = [[inventar_modulu['broadcaster'],PULZ_LOW,'tlacitko']]
    
    while pokracovat:
        
        hodiny+=1
        if DEBUG:
            print(f'Zpracovavam hodinovy TIK {hodiny}')
        ret_value = []
        #Nejdriv zpracuju vsechny vstupy
        for zaznam in pokracovat:
            zaznam[0].prijmi_vstup(zaznam[1],zaznam[2],hodiny)
        #nyni projdu vsechny vystpy a vygeneruji nove vstupy
        for modul in inventar_modulu.values():
            ret_value += modul.proved_vystup(hodiny)
        pokracovat = ret_value
    return hodiny
def analyze_frontu(inventar_modulu_simple,prvek,indent=0):
    fronta = []
    fronta.append(prvek)
    while True:
        nova_fronta = []
        for vecicka in fronta:
            print('-'*indent+ f'{vecicka}')
            for vstup in inventar_modulu_simple[vecicka].get('vstup'):
                nova_fronta.append(vstup)
        indent+=1
        fronta = nova_fronta
    
def main():
    inventar_modulu = {}
    inventar_modulu_simple = {}
    zasobnik_instrukci = []
    
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '#':
                break
            if line[0] == '%':
                inventar_modulu[line[1:].split(' -> ')[0]] = flip_flop(jmeno=line[1:].split(' -> ')[0])
                inventar_modulu_simple[line[1:].split(' -> ')[0]] = {'druh': line[0], 'vstupy':collections.deque(), 'vystup': None, 'vystupy':[], 'stav': STAV_OFF, 'vstup': []}
            elif line[0] == '&':
                inventar_modulu[line[1:].split(' -> ')[0]] = conjunction(jmeno=line[1:].split(' -> ')[0])
                inventar_modulu_simple[line[1:].split(' -> ')[0]] = {'druh': line[0], 'vstupy':collections.deque(), 'vystup': None, 'vystupy':[], 'stav':{}, 'vstup': []}
            elif line.startswith('broadcaster'):
                inventar_modulu['broadcaster'] = broadcaster(jmeno='broadcaster')
                inventar_modulu_simple[line.split(' -> ')[0]] = {'druh': 'broadcaster', 'vstupy':collections.deque(), 'vystup': None, 'vystupy':[], 'vstup': []}
            else:
                inventar_modulu[line.split(' -> ')[0]] = class_module(jmeno=line.split(' -> ')[0])
                inventar_modulu_simple[line.split(' -> ')[0]] = {'druh': None, 'vstupy':collections.deque(), 'vystup': None, 'vystupy':[], 'vstup': []}
            
            zasobnik_instrukci.append(line)
    propoj_moduly(inventar_modulu, zasobnik_instrukci, inventar_modulu_simple)
    hodiny = 1
    global DEBUG
    DEBUG= False
    vysledek1 = collections.Counter()
    vysledek2 = collections.Counter()
    for _ in range(1000):
    
        #hodiny = stiskni_tlacitko(inventar_modulu,hodiny)
        (counter1,counter2) = stiskni_tlacitko_simple(inventar_modulu_simple)
        vysledek2.update(counter2)
    
    print(f'Celkove statistiky jsou {vysledek2} a to dava {vysledek2[True]*vysledek2[False]}')    
    analyze_frontu(inventar_modulu_simple,'rx')
    return
    
    for jmeno, modul in dict(sorted(inventar_modulu.items())).items():
        print(f'Modul {jmeno}({modul.__class__.__name__}) mel input signaly:{modul.pocitadlo}, output signaly:{modul.pocitadlo_vystup}')
        vysledek.update(modul.pocitadlo)
    print(f'Celkove statistiky jsou {vysledek} a to dava {vysledek[True]*vysledek[False]}')
    #827027177 is too low
    
if __name__ == '__main__':
    main()