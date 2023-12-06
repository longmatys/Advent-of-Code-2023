import os
import math
def najdi_pocet_moznych_reseni(cas, vzdalenost):
    #Slo by to resit jako kvadraticka rovnice a bylo by to hnedka
    counter = 0
    for cas_pokusu in range(1,cas+1):
        cas_jizdy = (vzdalenost / cas_pokusu)
        if cas_jizdy + cas_pokusu < cas:
            print(f'candidate: {cas_pokusu}')
            counter+=1
    return counter
if __name__ == '__main__':
# Get the name of the Python script
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    casy= []
    distances = []
    vstupni_data = {
        'Time' : {'spojeni': '', 'fronta': []},
        'Distance': {'spojeni': '', 'fronta': []}
    }
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            print(line)
            if line=='#':
                break
            typ_vstupnich_dat = line.split(':')[0]
            
            for data in line.split(':')[1].split(' '):
                if data == '':
                    continue
                vstupni_data[typ_vstupnich_dat]['fronta'].append(int(data))
                vstupni_data[typ_vstupnich_dat]['spojeni']+=(data)
    celkovy_vysledek = 1
    for (cas, vzdalenost) in zip(vstupni_data['Time']['fronta'],vstupni_data['Distance']['fronta']):
        vysledek = najdi_pocet_moznych_reseni(cas, vzdalenost)
        print(f'Pocet kombinaci vitezstvi pro cas={cas} a vzdalenost={vzdalenost} je {vysledek}')
        celkovy_vysledek *= vysledek
    print(f'Celkova vaha kombinaci pro cast 1 je {celkovy_vysledek}') 
    #print(f"Celkova vaha kombinaci pro cast 2 je {najdi_pocet_moznych_reseni(int(vstupni_data['Time']['spojeni']),int(vstupni_data['Distance']['spojeni']))}") 