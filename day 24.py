import os
import logging
import itertools
def najdi_reseni_t(r,x,y):
    [(a,b,c),(px,py,pz)] = r
    t = (x - a) / px
    return t
def najdi_reseni_x(r,y):
    [(a,b,c),(px,py,pz)] = r
    x = px*(y - b) / py + a
    return x
def najdi_reseni_y(r1,r2):
    [(a1,b1,c1),(px1,py1,pz1)] = r1
    [(a2,b2,c2),(px2,py2,pz2)] = r2
    y = (px2*b2*py1 - px1*b1*py2 - a2*py1*py2 + a1*py1*py2) / (px2*py1 - px1*py2)
    return y
def najdi_reseni(r):
    (r1,r2) = r
    y = najdi_reseni_y(r1,r2)
    x = najdi_reseni_x(r1,y)
    t1 = najdi_reseni_t(r1, x, y)
    t2 = najdi_reseni_t(r2, x, y)
    return (x,y,t1,t2)
def parse_vector(line:str):
    #19, 13, 30 @ -2,  1, -2
    start = [int(cislo.strip()) for cislo in line.split('@')[0].split(',')]
    rychlost = [int(cislo.strip()) for cislo in line.split('@')[1].split(',')]
    return (start,rychlost)
MIN_RANGE = 200000000000000
MAX_RANGE = 400000000000000
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    zadani = []
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            zadani.append(parse_vector(line))
            if line == '#':
                break
            
    counter = 0
    for dvojice in itertools.combinations(zadani,2):
        try:
            #print(f'Dvojice {dvojice}',end='')
            (x,y,t1,t2) = najdi_reseni(dvojice)
            if t1 < 0 or t2 < 0:
                #print(f' ma reseni v minulosti (t1={t1},t2={t2})')
                ""
            elif x < MIN_RANGE or y < MIN_RANGE or x > MAX_RANGE or y > MAX_RANGE:
                #print(f' ma reseni mimo oblast (x={x},y={y})')
                ""
            else:
                counter+=1
                #print(f'Dvojice {dvojice} ma reseni (x={x},y={y})')
                
        except ZeroDivisionError:
            ""
            #print(f'Dvojice {dvojice} nema reseni')
    print(f'Pocet validnich reseni: {counter}')
if __name__ == '__main__':
    main()