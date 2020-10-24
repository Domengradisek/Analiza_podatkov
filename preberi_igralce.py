import re

with open('Podatki_o_igralcih.html', encoding='utf-8') as f:
    vsebina = f.read()

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

stevec = 0

for zadetek in re.finditer(vzorec, vsebina):
    print(zadetek.groupdict())
    stevec += 1

print(stevec)