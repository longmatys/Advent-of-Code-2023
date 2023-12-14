import os
import logging
def tiskni_mapu(mapa):
    for line in mapa:
        print(line)
def najdi_zrcadlo(line):
    return_set = set()
    for i in range(1,int(len(line))):
        part_r = line[i:2*i]
        part_r.reverse()
        if line[0:i] == part_r:
            return_set.add(i)
        part_r = line[len(line)-2*i:len(line)-i]
        part_r.reverse()
        if line[len(line)-i:] == part_r:
            return_set.add(len(line)-i)
    
    return return_set

def zpracuj_obrazek_lines(image):
    best_kandidat = None
    for line in image:
        kandidati = najdi_zrcadlo(list(line))
        if best_kandidat == None:
            best_kandidat = kandidati
        else:
            best_kandidat = best_kandidat.intersection(kandidati)
    return best_kandidat
def zpracuj_obrazek(image):
    osa_x = zpracuj_obrazek_lines(image)
    image_trans = list(map(list, zip(*image)))
    osa_y = zpracuj_obrazek_lines(image_trans)
    if osa_x and osa_y:
        return (osa_x, osa_y)
    if osa_x:
        return (osa_x,set())
    if osa_y:
        return (set(),osa_y)
    return (set(),set())
def zpracuj_obrazek_complex(image):
    vysledek = []
    souradnice = [None]
    reference = zpracuj_obrazek(image)
    for i,line in enumerate(image):
        for j,znak in enumerate(line):
            
            if znak == '#':
                new_znak = '.'
            else:
                new_znak = '#'
            line[j] = new_znak
            #vysledek.append([zpracuj_obrazek(image),i,j])
            vysledek = zpracuj_obrazek(image)
            #tiskni_mapu(image)
            #print(i,j,reference,vysledek)
            vysledek =(vysledek[0].difference(reference[0]), vysledek[1].difference(reference[1]))
            
            
            if vysledek != reference and (vysledek[0] or vysledek[1]):
                return vysledek
                if vysledek[0] == reference[0]:
                    return (0,vysledek[1])
                return (vysledek[0],0)
            line[j] = znak
    
    return (0,0)
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    vysledek = 0
    vysledek2 = 0
    with open(input_file) as f:
        image = []
        for line in f.readlines():
            line = line.strip()
            
            if line == '#':
                break
            image.append(list(line))
            if line == '':
                image.pop()
                mezivysledek = zpracuj_obrazek(image)
                if mezivysledek[0]:
                    vysledek+=mezivysledek[0].pop()
                if mezivysledek[1]:
                    vysledek+=mezivysledek[1].pop()*100
                mezivysledek = zpracuj_obrazek_complex(image)
                if mezivysledek[0]:
                    vysledek2+=mezivysledek[0].pop()
                if mezivysledek[1]:
                    vysledek2+=mezivysledek[1].pop()*100
                
                image = []
            print(line)
        mezivysledek = zpracuj_obrazek(image)
        if mezivysledek[0]:
            vysledek+=mezivysledek[0].pop()
        if mezivysledek[1]:
            vysledek+=mezivysledek[1].pop()*100
        mezivysledek = zpracuj_obrazek_complex(image)
        if mezivysledek[0]:
            vysledek2+=mezivysledek[0].pop()
        if mezivysledek[1]:
            vysledek2+=mezivysledek[1].pop()*100
        print(f'Part1: {vysledek}, Part2: {vysledek2}')
if __name__ == '__main__':
    main()