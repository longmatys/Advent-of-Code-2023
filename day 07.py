import os
import logging
vsechny_karty = ''.join(['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2'])
def hodnota_karty(karta):
    return len(vsechny_karty) - vsechny_karty.find(karta)
def spocitej_karty(balik):
    balik_pocty = {}
    for karta in balik:
        if not balik_pocty.get(hodnota_karty(karta)):
            balik_pocty[hodnota_karty(karta)] = 0
        balik_pocty[hodnota_karty(karta)] += 1
    return balik_pocty
varianty_baliku = ['Five of a kind', 'Four of a kind', 'Full house','Three of a kind','Two pair','One pair','High card']
def sila_baliku(balik):
    return len(varianty_baliku) - varianty_baliku.index(balik)
def vyhodnot_balik(balik):
    balik_spocitany = spocitej_karty(balik)
    karty_unikatni = len(balik_spocitany.keys())
    balik_spocitany_serazeny = sorted(balik_spocitany.items(),key=lambda x: (x[1],x[0]), reverse=True)
    if karty_unikatni == 1:
        return ['Five of a kind', balik_spocitany_serazeny[0]]
    if balik_spocitany_serazeny[0][1] == 4:
        return ['Four of a kind', balik_spocitany_serazeny[0]]
    if karty_unikatni == len(balik):
        return ['High card', balik_spocitany_serazeny[0]]
    if karty_unikatni == len(balik) - 1:
        return ['One pair', balik_spocitany_serazeny[0]]
    if (karty_unikatni == len(balik) - 2 and balik_spocitany_serazeny[0][1] == 3) or \
        (karty_unikatni == len(balik) - 3 and balik_spocitany_serazeny[0][1] == 2):
        return ['Three of a kind', balik_spocitany_serazeny[0]]
    if karty_unikatni == len(balik) - 2 and balik_spocitany_serazeny[0][1] == 2:
        return ['Two pair', balik_spocitany_serazeny[0]]
    if karty_unikatni == len(balik) - 3 and balik_spocitany_serazeny[0][1] == 3:
        return ['Full house', balik_spocitany_serazeny[0]]
    return None
def preloz_karty(balik):
    ret = []
    for karta in balik:
        ret+=[hodnota_karty(karta)]
    return ret
def main():
    #logging.basicConfig(level=logging.ERROR, format='%(funcName)s (%(lineno)d): %(message)s')
    logging.basicConfig(level=logging.ERROR, format='%(message)s')

# Get the name of the Python script
    script_name = os.path.basename(__file__)
    input_file = script_name.split('.')[0]+'.input.txt'
    vyhodnocene_baliky = []
    with open(input_file) as f:
        for line in f.readlines():
            line = line.strip()
            if line == '#':
                break
            logging.debug(line)
            
            ret = vyhodnot_balik(line.split(' ')[0])
            zaznam = [line.split(' ')[0], ret[0], int(line.split(' ')[1])]
            #zaznam = [sorted(line.split(' ')[0],reverse=True,key=lambda x: hodnota_karty(x)), ret[0], int(line.split(' ')[1])]
            #ty karty se NERADI!
            
            
            
            vyhodnocene_baliky.append(zaznam)
            logging.debug(f'Vyhodnocene zaznamy: {zaznam}')
    vysledek_hry = sorted(vyhodnocene_baliky,key=lambda x: (sila_baliku(x[1]),preloz_karty(x[0])))
    vyhra_celkem = 0
    for i,balik in enumerate(vysledek_hry):
        logging.error(f'{balik[0]} ,{balik}')
        vyhra_celkem += (i+1) * balik[2]
        logging.debug(f'Pocitam vyhru {i+1}.baliku ({balik[0]}) = {balik[1]} za {balik[2]} je celkem {(i+1)*balik[2]}. Celkova vyhra je {vyhra_celkem}')
    #logging.debug(vysledek_hry)
    print(f'Celkova vyhra: {vyhra_celkem}')
    #250660176 ... too high, pri razeni karet
    #249930103 ... too low
    #250118504 ... too low
if __name__ == '__main__':
    main()