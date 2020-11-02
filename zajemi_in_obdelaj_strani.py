import orodja
import re

vzorec_bloka = re.compile(
    f'<tr data-playerid=.*?'
    f' /></a></td></tr>',
    flags=re.DOTALL
)

vzorec_igralca = re.compile(
    r'<tr data-playerid="(?P<id>\d+?)">' # zajamemo ID igralca
    r'<td><figure class="player"><a href=".*?" '
    r'title="(?P<ime_in_priimek>.+?) FIFA 21" class="link-player">' # zajamemo ime igralca
    r'<img src=.*?</a></td>'
    r'<td data-title="Nationality"><a href="/players/\?nationality=\d.*?" title="(?P<državljanstvo>.+?)" class="link-nation">'# zajamemo državo
    r'<img src=".*? class="badge badge-dark rating .*?">'
    r'(?P<ocena>\d{2})' # ocena
    r'</span><span class="badge badge-dark rating .*?">'
    r'(?P<potencial>\d{2})' # potencial
    r'</span></td><td data-title="Name">.*?'
    r'<td data-title="Age">'
    r'(?P<starost>\d{2})'
    r'</td><td data-title="Hits">(?P<iskanja>\d+?)'
    r'</td><td data-title="Team">.*?'
    r'title="(?P<klub>.+?) FIFA 21".*?',
    flags=re.DOTALL
)

vzorec_igralnih_polozajev = re.compile(
    r'</td><td data-title="Preferred Positions" class="nowrap">(?P<igralni_polozaji>.*?)'
    r'</span></a></td>',
    flags=re.DOTALL
)

vzorec_igralnega_polozaja = re.compile(
    r'<a href="/players/.*? title="(?P<polozaj1>.+?)" class="link-position">.*?',
    flags=re.DOTALL
)

def izloci_igralne_polozaje(niz):
    igralni_polozaji = []
    for igralni_polozaj in vzorec_igralnega_polozaja.finditer(niz):
        x = igralni_polozaj.groupdict()['polozaj1']
        igralni_polozaji.append(x)
    return igralni_polozaji


def izloci_podatke_igralca(blok):
    igralec = vzorec_igralca.search(blok).groupdict()
    igralec['id'] = int(igralec['id'])
    igralec['ocena'] = int(igralec['ocena'])
    igralec['potencial'] = int(igralec['potencial'])
    igralec['starost'] = int(igralec['starost'])
    igralec['iskanja'] = int(igralec['iskanja'])
    #zdruzimo polozaje
    igralni_polozaji = vzorec_igralnih_polozajev.search(blok)
    if igralni_polozaji:
        igralec['polozaj1'] = izloci_igralne_polozaje(igralni_polozaji['igralni_polozaji'])
    return igralec




def igralci_na_strani(st_strani):
    url = f'https://www.fifaindex.com/players/{st_strani}/?gender=male&order=desc'
    ime_datoteke = 'zajeti-podatki/igralci{}.html'.format(st_strani)
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke)
    for blok in vzorec_bloka.finditer(vsebina):
        yield izloci_podatke_igralca(blok.group(0))


def izloci_gnezdene_podatke(igralci):
    polozaj1 = []

    for igralec in igralci:
        for polozaj in igralec.pop('polozaj1'):
            polozaj1.append({'igralec': igralec['id'], 'polozaj': polozaj})
    
    polozaj1.sort(key=lambda polozaj: (polozaj['igralec'], polozaj['polozaj']))

    return polozaj1


igralci = []
for st_strani in range(1,171):
    for igralec in igralci_na_strani(st_strani):
        igralci.append(igralec)
igralci.sort(key=lambda igralec: igralec['id'])
orodja.zapisi_json(igralci, 'obdelani-podatki/igralci.json')
polozaj1 = izloci_gnezdene_podatke(igralci)
orodja.zapisi_csv(
    igralci,
    ['id', 'ime_in_priimek', 'državljanstvo', 'ocena', 'potencial', 'starost', 'iskanja', 'klub'], 'obdelani-podatki/igralci.csv'
)
orodja.zapisi_csv(
    polozaj1,
    ['igralec', 'polozaj'], 'obdelani-podatki/polozaji.csv'
)