import os
import logging
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
def najdi_start(mapa,znak):
    for i,line in enumerate(mapa):
        try:
            return (i,line.index(znak))
        except ValueError:
            pass
    return None
def vypocitej_coord(mapa,point_from,offset_to):
    new_point =  (point_from[0]+offset_to[0],point_from[1]+offset_to[1])
    if new_point[0] < 0 or new_point[1] < 0 or new_point[0] == len(mapa) or new_point[1] == len(mapa[0]):
        return None
    return new_point       
def udelej_krok(mapa,startovni_body):
    ret_value = set()
    znackovacka = 'O'
    bod = startovni_body.pop()
    if mapa[bod[0]][bod[1]] == 'O':
        znackovacka = 'o'
        
    while bod:
        if mapa[bod[0]][bod[1]] != znackovacka:
            mapa[bod[0]][bod[1]] = '.' #Odejdu z daneho mista
        for smer in mapa_stran.keys():
            novy_bod = vypocitej_coord(mapa,bod,mapa_stran[smer]['to'])
            if novy_bod:
                if mapa[novy_bod[0]][novy_bod[1]] != '#':
                    mapa[novy_bod[0]][novy_bod[1]] = znackovacka
                    ret_value.add(novy_bod)
        if startovni_body:
            bod = startovni_body.pop()
        else:
            bod = None
    return ret_value
def tiskni_mapu(mapa):
    for line in mapa:
        print(line)
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    mapa = []
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()              
            mapa.append(list(line))
    nove_body = [najdi_start(mapa,'S')]
    for i in range(64):
        nove_body = udelej_krok(mapa,nove_body)
        #tiskni_mapu(mapa)
        #print(f'Nachazim se na {len(nove_body)} mistech\n')
    print(f'Nachazim se na {len(nove_body)} mistech\n')
if __name__ == '__main__':
    main()