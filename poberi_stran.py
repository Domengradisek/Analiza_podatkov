import requests
import re
import orodja


STEVILO_STRANI = 10

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
)

najdeni_igralci = 0

for stran in range(STEVILO_STRANI):
    count = stran + 1
    url = f'https://www.fifaindex.com/players/{count}/?gender=male&order=desc'
    datoteka = f'najboljsi_igralci/od_{30 * stran + 1}_do_{30 * stran + 30}.html'
    orodja.shrani_spletno_stran(url, datoteka)
    vsebina = orodja.vsebina_datoteke(datoteka)
    for zadetek in re.finditer(vzorec, vsebina):
        #print(zadetek.groupdict())
        najdeni_igralci += 1

print(najdeni_igralci)