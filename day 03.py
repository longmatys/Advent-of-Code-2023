import os
def check_for_symbol(schematic, i, j):
    if i < 0 or j < 0 or i > len(schematic)-1 or j > len(schematic[0]) -1:
        return (False,False)
    znak = schematic[i][j]
    if znak == '.' or znak.isnumeric():
        return (False,False)
    elif znak == '*':
        return (True,True)
    else:
        return (True, False)
    
if __name__ == '__main__':
# Get the name of the Python script
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    schematic = []
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#'):
                break
            schematic.append(line)
            
    global_counter = 0
    global_gear_magazine = {}
    for i in range(len(schematic)):
        j=0
        number = ''
        valid_part = False
        gears_magazine = {}
        while j < len(schematic[i]):
            if schematic[i][j].isnumeric():
                if number == '':
                    #Cislo zacina
                    for [ci,cj] in [[i-1,j-1],[i,j-1],[i+1,j-1]]:
                        (check_valid,check_gear) = check_for_symbol(schematic,ci,cj)
                        valid_part |= check_valid
                        if check_gear:
                            gears_magazine[(ci,cj)]=True
                    
                for [ci,cj] in [[i-1,j],[i+1,j]]:
                    (check_valid,check_gear) = check_for_symbol(schematic,ci,cj)
                    valid_part |= check_valid
                    if check_gear:
                        gears_magazine[(ci,cj)]=True
                
                
                number += schematic[i][j]
            else:
                #Cislo skoncilo
                for [ci,cj] in [[i-1,j],[i,j],[i+1,j]]:
                    (check_valid,check_gear) = check_for_symbol(schematic,ci,cj)
                    valid_part |= check_valid
                    if check_gear:
                        gears_magazine[(ci,cj)]=True
                
                if number != '' and valid_part:
                    global_counter += int(number)
                    for k in gears_magazine.keys():
                        if not global_gear_magazine.get(k):
                            global_gear_magazine[k] = []
                        global_gear_magazine[k].append(int(number))    
                number = ''
                valid_part = False
                gears_magazine = {}
            j+=1
        #Cislo konci na radku
        if number != '' and valid_part:
            global_counter += int(number)
        for k in gears_magazine.keys():
            if not global_gear_magazine.get(k):
                global_gear_magazine[k] = []
            global_gear_magazine[k].append(int(number))    
    global_counter_2 = 0
    for _,v in global_gear_magazine.items():
        if len(v) == 2:
            global_counter_2 += v[0]*v[1]
    print(global_counter, global_counter_2)
        
            
            
                
        