import os
def get_intersect_right(id_a,len_a,id_b,len_b):
    rozdil = id_b - id_a
    if (rozdil >= len_b):
        return((id_b,len_b),(None,None))
    else:
        return((id_b,len_a - rozdil),(id_b+(len_a-rozdil),len_b-(len_a-rozdil)))
def get_intersect_left(id_a,len_a,id_b,len_b):
    rozdil = id_b - id_a
    #len1 = id - id_a
    if rozdil >= len_a:
        return((id_a,len_a),(None,None),(None,None))
    elif id_a+len_a <= id_b+len_b:
        return((id_a,(id_b-id_a)),(id_b,len_a-(id_b-id_a)),(None,None))
    else:
        return((id_a,(id_b-id_a)),(id_b,len_b),(id_b+len_b,len_a-len_b-(id_b-id_a)))
    
def find_dest_by_range(maps,id,delka,dst):
    #rid ... (id,len)
    #print(f'Trying {id}, {delka}, {dst}')
    if dst == 'END':
        return id
    if delka < 0:
        ""
    (last_id,last_len) = (0,0)
    new_id = None
    new_left_value = None
    new_mid_value = None
    new_right_value = None
    for id_candidate in sorted(maps[dst].keys()):
        
        if id_candidate > id:
            #at least some are within range
            if id < last_id + last_len:
                #is within defined range
                
                ((left_id,left_len),(right_id,right_len)) = get_intersect_right(last_id,last_len,id,delka)
                new_left_value = find_dest_by_range(maps,
                                                    maps[dst][last_id]['dst'] + (left_id - last_id),
                                                    left_len,
                                                    maps['trans'][dst])
                
                if right_id:
                    new_right_value = find_dest_by_range(maps,right_id,right_len,dst)
                break
            elif id < id_candidate + maps[dst][id_candidate]['len']:
                ((left_id,left_len),(mid_id,mid_len),(right_id,right_len)) = get_intersect_left(id,delka,id_candidate,maps[dst][id_candidate]['len'])
                new_left_value = find_dest_by_range(maps,
                                                    left_id,
                                                    left_len,
                                                    maps['trans'][dst])
                if mid_id:
                    new_mid_value = find_dest_by_range(maps,
                                                    maps[dst][id_candidate]['dst'],
                                                    mid_len,
                                                    maps['trans'][dst])
                if right_id:
                    new_right_value = find_dest_by_range(maps,
                                                    right_id,
                                                    right_len,
                                                    dst)
                break
            else:
                "No translate, but go for another candidate"
        else:
            #For easy code same as above
            (last_id, last_len) = (id_candidate, maps[dst][id_candidate]['len'])
            
            if id < last_id + last_len:
                #is within defined range
                
                ((left_id,left_len),(right_id,right_len)) = get_intersect_right(last_id,last_len,id,delka)
                new_left_value = find_dest_by_range(maps,
                                                    maps[dst][last_id]['dst'] + (left_id - last_id),
                                                    left_len,
                                                    maps['trans'][dst])
                
                if right_id:
                    new_right_value = find_dest_by_range(maps,right_id,right_len,dst)
                break    
    result_candidates = []
    if new_left_value:
        result_candidates.append(new_left_value)
    if new_mid_value:
        result_candidates.append(new_mid_value)
    if new_right_value:
        result_candidates.append(new_right_value)
    if len(result_candidates):
        return min(result_candidates)
        
    
    return find_dest_by_range(maps,id,delka,maps['trans'][dst])
def find_dest(maps,id,src,dst):
    print(id,src,dst)
    (last_id,last_len) = (0,0)
    new_id = None
    for id_candidate in sorted(maps[dst].keys()):
        if id_candidate > id:
            if id < last_id + last_len:
                new_id = maps[dst][last_id]['dst'] + (id - last_id)
                break
            else:
                new_id = id
        else:
            (last_id, last_len) = (id_candidate, maps[dst][id_candidate]['len'])
            if id < last_id + last_len:
                new_id = maps[dst][last_id]['dst'] + (id - last_id)
                break
            else:
                "Search next"
    if not new_id:
        "Vubec jsem to nenasel"
        new_id = id      
    if dst == 'location':
        return (new_id)
    return (find_dest(maps,new_id,dst,maps['trans'][dst]))
            
        
def main():
    t = get_intersect_left(18,10,20,3)
    t = get_intersect_left(18,5,20,3)
    t = get_intersect_left(18,5,30,3)
    t = get_intersect_right(20,10,28,10)
    t = get_intersect_right(20,10,22,2)
    # Get the name of the Python script
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    schematic = []
    maps = {
        'seeds': [],
        'trans': {'location': 'END'}
    }
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#'):
                break
            if line == '':
                continue
            if line.endswith('map:'):
                descriptor = line.split(' ')[0].split('-')
                maps[descriptor[2]] = {}
                maps['trans'][descriptor[0]] = descriptor[2]
                ""
            elif line.startswith('seeds:'):
                print(line.split(':')[1].split(' '))
                for seed in line.split(':')[1].split(' '):
                    if seed == '':
                        continue
                    maps['seeds'].append(int(seed))
            else:
                line_a = line.split(' ')
                maps[descriptor[2]][int(line_a[1])] = {
                    'len': int(line_a[2]),
                    'dst': int(line_a[0])
                }
    lowest = None
    for seed in maps['seeds']:
        result = find_dest(maps,seed,'seeds',maps['trans']['seed'])
        print(result)
        if not lowest or (result < lowest):
            lowest = result
    print('Part 1:',lowest)
    lowest = None
    for i in range(0,len(maps['seeds']),2):
        print(f'Processing {i}')
        #for seed_offset in range(maps['seeds'][i+1]):
        result = find_dest_by_range(maps,maps['seeds'][i],maps['seeds'][i+1],maps['trans']['seed'])
        if not lowest or (result < lowest):
            lowest = result
    print('Part 2:',lowest)
if __name__ == '__main__':
    main()