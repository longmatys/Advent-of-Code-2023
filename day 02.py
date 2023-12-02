import os
if __name__ == '__main__':
# Get the name of the Python script
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    output_wires = {}
    towns = {}
    ways = {}
    counter = 0
    game_cubes = {
                'red': 12,
                'green': 13,
                'blue': 14
            }
    counter_id = 0
    power_global = 0
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            
            gameid = int(line.split(':')[0].split(' ')[1])
            throws = line.split(':')[1].split(';')
            most_cubes = {
                'red': 0,
                'green': 0,
                'blue': 0
            }
            for throw in throws:
                throw = throw.strip()
                for cube in throw.split(','):
                    cube = cube.strip()
                    cube_parts = cube.split(' ')
                    #print(gameid,throw,cube,cube_parts)
                    if most_cubes[cube_parts[1]] < int(cube_parts[0]):
                        most_cubes[cube_parts[1]] = int(cube_parts[0])
            valid_game = True
            for k,v in game_cubes.items():
                if most_cubes[k] > v:
                    valid_game = False
                    break
            if valid_game:
                counter_id += gameid
            power_local = 1
            for k,v in most_cubes.items():
                power_local *= v
            power_global += power_local
            print(gameid,game_cubes,most_cubes,valid_game, power_local)
    print(f'Soucet validnich her: {counter_id}, Power vsech her: {power_global}')