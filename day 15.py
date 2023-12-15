import os
import logging
import collections
def spocitej_hash(element):
    hodnota = 0
    for znak in element:
        hodnota = ((hodnota+ord(znak))*17) % 256
    return hodnota
def spocitej_radku(line:str):
    vysledky = []
    vysledky2 = 0
    lenses = {}
    boxy = [collections.deque() for _ in range(256) ]
    for element in line.split(','):
        
        if element[-1] == '-':
            cislo_boxu = spocitej_hash(element[:-1])
            try:
                boxy[cislo_boxu].remove(element[:-1])
            except ValueError:
                pass
        else:
            cislo_boxu = spocitej_hash(element[:-2])
            lenses[element[:-2]] = element[-1]
            if element[:-2] not in boxy[cislo_boxu]:
                boxy[cislo_boxu].append(element[:-2])
                
            
            
        vysledky.append(spocitej_hash(element))
    for box_id, box in enumerate(boxy):
        for box_slot_id,len_name in enumerate(box):
            vysledky2 += (box_id+1) * (box_slot_id+1) * int(lenses[len_name])
    return (sum(vysledky),vysledky2)

def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            (vysledek,vysledek2) = spocitej_radku(line)
            print(f'Vysledek je Part1: {vysledek}, Part2: {vysledek2}')
if __name__ == '__main__':
    main()