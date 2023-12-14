import os
import logging
import collections
import alive_progress
def tiskni_mapu(mapa):
    print(f'Vytisk mapy')
    for line in mapa:
        print(line)
def vypocitej_sever(mapa):
    vypocet = 0
    for i,line in enumerate(mapa):
        pocet = collections.Counter(line).get('O')
        if pocet:
            vypocet += pocet * (len(mapa)-i)
    return vypocet
    #print(f"Celkova vaha je {vypocet}")
def pokus_se_najit_periodu(pole,perioda = 5):
    for i in range(1,int(len(pole)/(perioda))):
        vzorek = pole[-i:]
        vzorek_plny = vzorek * perioda
        if vzorek_plny == pole[-i*perioda:]:
            return (i,vzorek)
    return None
#pokus_se_najit_periodu([1, 2, 3, 4, 5, 6, 7, 8, 9, 6, 7, 8, 9, 6, 8, 8, 9, 6, 7, 8, 9])
def sesyp_kameny_jina_metoda(mapa,cycles_max=1):
    #Nejdriv transponovat mapu
    smer_index = 0
    vysledky = []
    smery = ['N','W','S','E']
    sloupec_index_max = len(mapa[0])
    radek_index_max = len(mapa)
    with alive_progress.alive_bar(cycles_max) as bar:
        for cycle in range(1,cycles_max+1):
            if cycle % 100 == 0:
                bar(100)
            smer = smery[smer_index]
            smer_index = (smer_index + 1) % len(smery)
            if smer == 'N':
                for sloupec_index in range(sloupec_index_max):
                    for radek_index in range(1,radek_index_max):
                        if mapa[radek_index][sloupec_index] == 'O':
                            j = 1
                            while radek_index >= j and mapa[radek_index - j][sloupec_index] == '.':
                                mapa[radek_index - (j-1)][sloupec_index] = '.'
                                j+=1
                            mapa[radek_index - (j-1)][sloupec_index] = 'O'
            elif smer == 'S':
                for sloupec_index in range(sloupec_index_max):
                    for radek_index in range(1,radek_index_max):
                        if mapa[radek_index_max-1 - radek_index][sloupec_index] == 'O':
                            j = 1
                            while radek_index >= j and mapa[radek_index_max-1 - (radek_index - j)][sloupec_index] == '.':
                                mapa[radek_index_max-1 - (radek_index - (j-1))][sloupec_index] = '.'
                                j+=1
                            mapa[radek_index_max-1 - (radek_index - (j-1))][sloupec_index] = 'O'
            elif smer == 'W':
                for radek_index in range(radek_index_max):
                    for sloupec_index in range(1,sloupec_index_max):
                        if mapa[radek_index][sloupec_index] == 'O':
                            j = 1
                            while sloupec_index >= j and mapa[radek_index][sloupec_index-j] == '.':
                                mapa[radek_index ][sloupec_index - (j-1)] = '.'
                                j+=1
                            mapa[radek_index][sloupec_index - (j-1)] = 'O'
            elif smer == 'E':
                for radek_index in range(radek_index_max):
                    for sloupec_index in range(1,sloupec_index_max):
                        if mapa[radek_index][sloupec_index_max -1 - sloupec_index] == 'O':
                            j = 1
                            while sloupec_index >= j and mapa[radek_index][sloupec_index_max -1 - (sloupec_index-j)] == '.':
                                mapa[radek_index ][sloupec_index_max -1 - (sloupec_index-(j-1))] = '.'
                                j+=1
                            mapa[radek_index][sloupec_index_max -1 - (sloupec_index-(j-1))] = 'O'
            
            #if smer == 'N':
            #tiskni_mapu(mapa)
            #c = collections.Counter()
            #for item in mapa:
            #    c.update(item)
            vypocet = vypocitej_sever(mapa)
            
            #if smer == 'E':
            #    tiskni_mapu(mapa)
            vysledky.append(f'{smer}:{vypocet}')
            if smer == 'E':
                c = 5
                v = pokus_se_najit_periodu(vysledky,c)
                if v != None:
                    #print(f'Perioda {v}',vysledky)
                    print(f'Perioda {v[0]}, cycle: {cycle//4}')
                    
                    celkem = 1000000000
                    posun = (celkem-(cycle//4))%(v[0]//4)
                    print(f'Po {celkem} cyklech bude vaha {v[1][posun*4-1]} ve finale')
                    return
                    z=0
                    #return
            #print(f'Projel jsem smer {smer} a mam vahu {vypocet}')
            #z=1
def sesyp_kameny(mapa):
    #Nejdriv transponovat mapu
    mapa_trans = list(map(list, zip(*mapa)))
    for line in mapa_trans:
        for i in range(1,len(line)):
            if line[i] == 'O':
                j = 1
                while i>=j and line[i-j]=='.':
                    line[i-(j-1)] = '.'
                    j+=1    
                line[i-(j-1)] = 'O'
    mapa = list(map(list, zip(*mapa_trans)))
    print(f'Part 1: {vypocitej_sever(mapa)}')
    #tiskni_mapu(mapa)
    


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
            #print(line)
            mapa.append(list(line))
    #tiskni_mapu(mapa)
    sesyp_kameny(mapa)
    sesyp_kameny_jina_metoda(mapa,1000000000)
    
    
if __name__ == '__main__':
    main()