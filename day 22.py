import os
import logging
import collections
KOSTKA_ID = ord('A')-1
def vloz_kostku(mapa:list,kostka:list):
    ""
def vytvor_kostku(line:str) -> list:
    global KOSTKA_ID
    
    (x1,y1,z1) = [int(dim) for dim in line.split('~')[0].split(',')]
    (x2,y2,z2) = [int(dim) for dim in line.split('~')[1].split(',')]
    x_dimension = abs(x2-x1)+1
    y_dimension = abs(y2-y1)+1
    z_dimension = abs(z2-z1)+1
    a = range(1,5)
    
    KOSTKA_ID+=1
    return (KOSTKA_ID,[min(x1,x2),min(y1,y2),min(z1,z2)],[max(x1,x2),max(y1,y2),max(z1,z2)])
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    kostky = collections.deque()
    body_x = []
    body_y = []
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '#':
                break
            (id_kostky,kostka_min_bod,kostka_max_bod) = vytvor_kostku(line)
            body_x+=[kostka_min_bod[0],kostka_max_bod[0]]
            body_y+=[kostka_min_bod[1],kostka_max_bod[1]]
            rozsah_x = range(kostka_min_bod[0],kostka_max_bod[0]+1)
            rozsah_y = range(kostka_min_bod[1],kostka_max_bod[1]+1)
            vyska = kostka_max_bod[2] - kostka_min_bod[2] + 1
            start_vyska = kostka_min_bod[2]
            
            kostky.append((id_kostky,rozsah_x,rozsah_y,vyska,start_vyska))
    patra = []
    globalni_kolize = {}
    patra_kostky_start = {}
    for kostka in sorted(kostky,key= lambda x: x[4]):
        (id_kostky,rozsah_x,rozsah_y,vyska,start_vyska) = kostka
        globalni_kolize[id_kostky] = {'zavisli_na':set(), 'podpora_pro':set()}
        skoncit = False
        aktualni_patro = -1
        for aktualni_patro in range(len(patra)):
            for rozsah in patra[-(aktualni_patro+1)]:
                if set(rozsah[1])&set(rozsah_x) and set(rozsah[2])&set(rozsah_y):
                    globalni_kolize[id_kostky]['zavisli_na'].add(rozsah[0])
                    globalni_kolize[rozsah[0]]['podpora_pro'].add(id_kostky)
                    skoncit = True
            if skoncit:
                break
        if skoncit:
            aktualni_patro -=1
        if aktualni_patro < 0:
            globalni_kolize[id_kostky]['patro'] = len(patra)-1+1
        else:
            globalni_kolize[id_kostky]['patro'] = len(patra)-(aktualni_patro+1)
        if not patra_kostky_start.get(globalni_kolize[id_kostky]['patro']):
            patra_kostky_start[globalni_kolize[id_kostky]['patro']]=0
        patra_kostky_start[globalni_kolize[id_kostky]['patro']]+=1
        for i in range(vyska):
            
            if aktualni_patro < 0:
                patra.append([])
                patra[-1].append((id_kostky,rozsah_x,rozsah_y))
            else:
                patra[-(aktualni_patro+1)+i].append((id_kostky,rozsah_x,rozsah_y))
            aktualni_patro -= 1
        
    nesmi_se_odebrat = set([item for k,v in globalni_kolize.items() for item in v['zavisli_na'] if len(v['zavisli_na'])==1])
    #print(nesmi_se_odebrat)
    print('Pocet kostek, co se mohou odebrat:', len(globalni_kolize)-len(nesmi_se_odebrat))
    spadlych_kostek = 0
    pocitadlo = 0
    
    for kostka_beru in nesmi_se_odebrat:
        #kostka_beru = 1297
        odebrane_kostky = [kostka_beru]
        chybejici_kostky = set()
        while odebrane_kostky:
            kostka = odebrane_kostky.pop()
            chybejici_kostky.add(kostka)
            for kandidat in globalni_kolize[kostka]['podpora_pro']:
                if globalni_kolize[kandidat]['zavisli_na'] & chybejici_kostky == globalni_kolize[kandidat]['zavisli_na']:
                    odebrane_kostky.append(kandidat)
        print(f'Pri odebrani kostky {kostka_beru} spadne {len(chybejici_kostky)-1}')
        pocitadlo+=len(chybejici_kostky)-1
    print(f'Po odebrani {len(nesmi_se_odebrat)} kritickych kostek spadne {pocitadlo} kostek')
    #77383 is too high
if __name__ == '__main__':
    main()