import os
def find_left(retez):
    for i in range(len(retez)):
        if retez[i].isnumeric():
            return (i,int(retez[i]))
def find_right(retez):
    for i in range(len(retez)):
        if retez[len(retez)-1-i].isnumeric():
            return (len(retez)-1-i,int(retez[len(retez)-1-i]))

cisla = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}
def find_str_left(retez):
    best_position = len(retez)+1
    best_number = None
    for cislo in cisla.keys():
        position = retez.find(cislo)
        if position > -1 and best_position > position:
            best_position = position
            best_number = cisla[cislo]
    return (best_position,best_number)
def find_str_right(retez):
    best_position = -1
    best_number = None
    for cislo in cisla.keys():
        position = retez.rfind(cislo)
        if position > -1 and best_position < position:
            best_position = position
            best_number = cisla[cislo]
    return (best_position,best_number)
if __name__ == '__main__':
# Get the name of the Python script
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    output_wires = {}
    towns = {}
    ways = {}
    counter = 0
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            find_l_1 = find_left(line)
            find_l_2 = find_str_left(line)
            
            if find_l_1[0] < find_l_2[0]:
                find_l = find_l_1[1]
            else:
                find_l = find_l_2[1]
            find_r_1 = find_right(line)
            find_r_2 = find_str_right(line)
            if find_r_1[0] > find_r_2[0]:
                find_r = find_r_1[1]
            else:
                find_r = find_r_2[1]
            counter+= find_l*10 + find_r
            
            
print(counter)


