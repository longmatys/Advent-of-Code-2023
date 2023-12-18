import os
import logging
def aktualizuj_rohy(rohy, point):
    rohy[0][0] = min(rohy[0][0],point[0])
    rohy[1][0] = max(rohy[1][0],point[0])
    rohy[0][1] = min(rohy[0][1],point[1])
    rohy[1][1] = max(rohy[1][1],point[1])
def aktulizuj_point(point,krok):
    match krok[0]:
        case 'R':
            point[1]+=int(krok[2]) 
        case 'L':
            point[1]-=int(krok[2])             
        case 'D':
            point[0]+=int(krok[2])             
        case 'U':
            point[0]-=int(krok[2]) 
            
def najdi_rohy(kroky:list):
    point = [0,0]
    rohy = [[0,0],[0,0]]
    for krok in kroky:
        aktulizuj_point(point,krok)
        aktualizuj_rohy(rohy,point)
    return rohy
def nakresli_znak(mapa,point,znak):
    mapa[point[0]][point[1]] = znak
def nakresli_kroky(mapa:list,kroky:list):
    point = [1,1]
    nakresli_znak(mapa,point,'#')
    for krok in kroky:
        match krok[0]:
            case 'R':
                for _ in range(int(krok[2])*2+1):
                    point[1]+=1
                    nakresli_znak(mapa,point,'#')
            case 'L':
                for _ in range(int(krok[2])*2+1):
                    point[1]-=1
                    nakresli_znak(mapa,point,'#')
            case 'D':
                for _ in range(int(krok[2])*2+1):
                    point[0]+=1
                    nakresli_znak(mapa,point,'#')
            case 'U':
                for _ in range(int(krok[2])*2+1):
                    point[0]-=1
                    nakresli_znak(mapa,point,'#')
def main():
# Get the name of the Python script
    logging.basicConfig(level=logging.DEBUG, format='%(funcName)s (%(lineno)d): %(message)s')
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    kroky = []
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            kroky.append(line)
    rohy = najdi_rohy(kroky)
    mapa = [['.']*(abs(rohy[1][1]-rohy[0][1])+3)*2 for _ in range((abs(rohy[1][0]-rohy[0][0])+3)*2)]
    print(rohy)
    nakresli_kroky(mapa,kroky)
    print(1)
if __name__ == '__main__':
    main()