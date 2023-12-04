import os
import json
def increment_multis(multis, current, count=1):
    if not multis.get(current):
        multis[current] = 0
    multis[current] += count
if __name__ == '__main__':
# Get the name of the Python script
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    schematic = []
    counter = 0
    multis = {}
    current = 1
    cards = 0
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#'):
                break
            line = line.replace('  ', ' ')
            set_1 = set(line.split(':')[1].split('|')[0].strip().split(' '))
            set_2 = set(line.split(':')[1].split('|')[1].strip().split(' '))
            pocet = len(set_1 & set_2)
            worth = 0
            
            increment_multis(multis, current)
            if pocet :
                for i in range(current+1,current+1+pocet):
                    increment_multis(multis, i, multis[current])
                worth = 2**(pocet-1) * multis[current]
            
            cards+=multis[current]
            counter+=worth
            print(line, set_1, set_2, f'Count:{pocet}', worth, current, multis.get(current))
            print(json.dumps(multis, indent=2))
            current+=1
    print(f'counter:{counter}, cards:{cards}')