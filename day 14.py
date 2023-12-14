import os
import logging
import collections
def tiskni_mapu(mapa):
    for line in mapa:
        print(line)
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
    tiskni_mapu(mapa)
    vypocet = 0
    for i,line in enumerate(mapa):
        pocet = collections.Counter(line).get('O')
        if pocet:
            vypocet += pocet * (len(mapa)-i)
    print(f"Celkova vaha je {vypocet}")


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
            mapa.append(line)
    tiskni_mapu(mapa)
    sesyp_kameny(mapa)
    
if __name__ == '__main__':
    main()