import os
from collections import Counter
import math
def spocitej_cestu(mapa,uzel_in,instrukce,koncovy_uzel='ZZZ',min_delka = None, max_offset=0):
    
    if uzel_in[1] < 0 or uzel_in[3]<0:
        print(uzel_in)
    offset = uzel_in[1]
    uzel = uzel_in[0]
    if offset < 0:
        offset = 0
    konec = False
    counter = 0
    if offset == max_offset and offset != 0:
        return uzel_in
    if uzel_in[0] == uzel_in[2]:
        if uzel_in[1] == uzel_in[3]:
            return uzel_in
        return [uzel, 2* uzel_in[1] - uzel_in[3], uzel_in[0], uzel_in[1]] 
    while not konec:
        for i, ins in enumerate(instrukce):
            uzel = mapa[uzel][ins]
            if uzel.endswith(koncovy_uzel):
                if min_delka:
                    if min_delka <= counter*len(instrukce)+i+1 + offset:
                        konec = True
                        break
                else:
                    konec = True
                    break
        if not konec:
            counter+=1
    vys = counter*len(instrukce)+i+1
    return [uzel, counter*len(instrukce)+i+1 + offset, uzel_in[0], uzel_in[1]] 

    #print(f'Vysledek : {counter*len(instructions)+i+1}',counter, i, len(instructions))
def find_gcd_of_array(arr):
    result_gcd = arr[0]
    for element in arr[1:]:
        result_gcd = math.gcd(result_gcd, element)
    return result_gcd
def find_lcm_of_array(arr):
    def find_gcd(a, b):
        return abs(math.gcd(a, b))

    def find_lcm(a, b):
        return abs(a * b) // find_gcd(a, b) if a and b else 0

    result_lcm = arr[0]
    for element in arr[1:]:
        result_lcm = find_lcm(result_lcm, element)
    return result_lcm
def hledej_rychle(vstup):
    print(vstup)
    pole = [int(it[1]/(it[1]/(it[1]-it[3]))) for it in vstup]
    vysledek = find_lcm_of_array(pole)
    
    print(f'Reseni Part 2 je {vysledek}')
def main():
# Get the name of the Python script
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    instrukce = None
    mapa = {}
    starts = []
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '#':
                break
            if line == '':
                continue
            if not instrukce:
                instrukce = line
            else:
                #AAA = (BBB, BBB)
                klic = line.split(' = ')[0]
                L = line.split('(')[1].split(',')[0]
                R = line.split(', ')[1][:-1]
                mapa[klic] = {'L':L, 'R':R}
                if klic.endswith('A'):
                    starts.append([klic,0,'.',0])
            #print(line)
    
    
    #print(f'Vysledek : {spocitej_cestu(mapa,"11A",instrukce,"Z")}')
    konec = False
    nejdelsi = 1
    vysledky = {
        
    }
    
    vysledky_kolo = starts
    opakovacka = False
    while not konec and not opakovacka:
        starts = vysledky_kolo
        max_offset = max(it[1] for it in starts)
        vysledky_kolo = [spocitej_cestu(mapa,klic_t,instrukce,'Z',max_offset=max_offset) for klic_t in starts]
        #print(f'Vysledek kola: {vysledky_kolo}')
        opakovacka = min([it[0] == it[2] for it in vysledky_kolo])
        
        konec = max(it[1] for it in vysledky_kolo) == min(it[1] for it in vysledky_kolo)
        a= 1
    #22357 is too low
    #66509 is too low
    #1941946 is too low
    if not konec:
        hledej_rychle(vysledky_kolo)
    else:
        print(f'Vysledek Part 2 = {vysledky_kolo}',vysledky_kolo[0][1])
if __name__ == '__main__':
    main()