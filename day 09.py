import os
import logging
import collections

    
def reduce_line(line:list) -> list:
    logging.debug(f'Redukuji seznam {line}')
    if len(collections.Counter(line).keys()) == 1 and list(collections.Counter(line).keys())[0] == 0:
        return [0,0]
    ret_value = reduce_line([line[i+1]-line[i] for i in range(len(line) -1)])
    ret_value = [ ret_value[0] + line[-1], line[0] - ret_value[1]]
    logging.debug(f'Vysledek vraci {ret_value}')
    return ret_value

def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    vysledek = [0,0]
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '#':
                break
            logging.debug(line)
            mezivysledek = reduce_line([int(cislo) for cislo in line.split(' ')])
            
            print(line, f'Meziysledek= {mezivysledek}')
            vysledek = [vysledek[i]+v for i,v in enumerate(mezivysledek)]
            
            
        print(line, f'Vysledek= {vysledek}')
        #1904165829 too high
        #1904165718
if __name__ == '__main__':
    main()