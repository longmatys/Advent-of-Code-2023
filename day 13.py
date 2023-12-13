import os
import logging
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
    if osa_x:
        return osa_x.pop()
    
    return osa_y.pop()*100
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    vysledek = 0
    with open(input_file) as f:
        image = []
        for line in f.readlines():
            line = line.strip()
            
            if line == '#':
                break
            image.append(line)
            if line == '':
                image.pop()
                vysledek+=zpracuj_obrazek(image)
                image = []
            print(line)
        vysledek+=zpracuj_obrazek(image)
        print(vysledek)
if __name__ == '__main__':
    main()