import requests
import re
import orodja


STEVILO_STRANI = 2

vzorec = (
    r'<tr data-playerid="(?P<id>\d*?)">' # zajamemo ID igralca
    r'<td><figure class="player"><a href=".*?" '
    r'title="(?P<ime_in_priiimek>.*?) FIFA 21" class="link-player">' # zajamemo ime igralca
    r'<img src=.*?</a></td>'
    r'<td data-title="Nationality"><a href="/players/\?nationality=\d.*?" title="(?P<država>.*?)" class="link-nation">'# zajamemo državo
    r'<img src=".*? class="badge badge-dark rating .*?">'
    r'(?P<kakovost>\d{2})' # kakovost
    r'</span><span class="badge badge-dark rating .*?">'
    r'(?P<potencial>\d{2})' # potencial
    r'</span></td><td data-title="Name">.*?'
    r'<td data-title="Preferred Positions".*?title="'
    r'(?P<polozaj_1>.*?)" class="link-position">'
    r'<span .*?</span>'
    r'(</a><a href.*? title="(?P<polozaj_2>.*?)" class="link-position"><span .*?</span>)?'
    r'(</a><a href.*? title="(?P<polozaj_3>.*?)" class="link-position"><span .*?</span>)?'
    r'</a></td><td data-title="Age">'
    r'(?P<starost>\d{2})'
    r'</td><td data-title="Hits">(?P<iskanja>\d*?)'
    r'</td><td data-title="Team">.*?'
    r'title="(?P<klub>.*?) FIFA 21".*?'
)

najdeni_igralci = 0

for stran in range(STEVILO_STRANI):
    count = stran + 1
    url = f'https://www.fifaindex.com/players/{count}/?gender=male&order=desc'
    datoteka = f'najboljsi_igralci/od_{30 * stran + 1}_do_{30 * stran + 30}.html'
    orodja.shrani_spletno_stran(url, datoteka)
    vsebina = orodja.vsebina_datoteke(datoteka)
    for zadetek in re.finditer(vzorec, vsebina):
        print(zadetek.groupdict())
        najdeni_igralci += 1

print(najdeni_igralci)