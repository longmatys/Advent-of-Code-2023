import os
import re

def replace_consecutive_dots(input_string):
    # Use re.sub to replace any occurrences of one or more dots with a single dot
    return re.sub(r'\.+', '.', input_string)


def kyble(tup):
    (pattern, springs) = tup
    springs = list(map(int,springs.split(',')))
    print(tup)
    line_new = replace_consecutive_dots(pattern)
    lpatt = line_new.split('.')
    return search(lpatt[0],lpatt,1,springs,0)
def get_rest(arr,arr_i):
    if len(arr)-1>arr_i:
        return arr[arr_i]
def search(work,instr,instr_i,springs,springs_i):
    counter=0

    for j in range(len(instr)+1-instr_i):
        for i in range(len(work)+1-springs[springs_i]):
            m = re.match(r"[\?#]{{{}}}([^#]?)(.*)".format(springs[springs_i]),work[i:])
            if m:
                if len(springs) - 1 == springs_i:   #No more springs to find
                    if len(instr) - 1 >= instr_i+j:
                        rest = instr[instr_i+j:]
                    else:
                        rest = []
                    if len([x for x in [m[1]]+rest if x.find('#')>=0])>0:   #No more springs, but still in map
                        counter += 0
                    else:
                        counter += 1
                        
                elif len(m[1])>0 and len(m[2]) >= springs[springs_i+1]:    #Can the rest of work hold next spring?
                    #continue in work
                    counter+=search(m[2],instr,instr_i+j,springs,springs_i+1)
                elif len(instr) == instr_i+j:   #No more maps of springs but still some to find
                    counter+=0
                else:
                    counter+=search(instr[instr_i+j],instr,instr_i+j+1,springs,springs_i+1)
                    
                if work[i]=='#':
                    break
            else: #Actual springs can not fit in work
                break
        if instr_i+j < len(instr):
            work = instr[instr_i+j]
    
    return counter
def rozsir_radek(radka:str, extended:int = 1):
    radka = radka.strip()
    zadani_z = radka.split(' ')[0]
    #pocty_z = ','.join([int(pocet) for pocet in radka.split(' ')[1].split(',')])
    pocty_z = radka.split(' ')[1]
    
    zadani = '?'.join([zadani_z for _ in range(extended)])
    pocty = ','.join([pocet for pocet in ','.join([pocty_z for _ in range(extended)]).split(',')])
    return ' '.join([zadani,pocty])
def main():
    
# Get the name of the Python script
    
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    pocitadlo = 0
    pocitadlo2 = 0
    print('Zacatek')
    with open(input_file) as f:
        #with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
        #    results = list(executor.map(kyblikova_metoda_mp, f.readlines()))
        all = 0
        for line in f.readlines():
            res = kyble(line.strip().split(' '))
            print(line.strip(),'Pocet kombinace:',res)
            all+=res
        print('Final:',all)
            
        
    #print(results)
    #print(sum(results))
    print(f'Part1: {pocitadlo}')
    print(f'Part2: {pocitadlo2}')
if __name__ == '__main__':
    print()
    a = ['aaa','aba']
    b = len([x for x in a if x.find('b')>=0])
    print(b)
    main()
    t = '????'
    m = re.match(r"[\?#]{2}.?(.*)",t)
    print(m.groups(),m[1])