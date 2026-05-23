#! /usr/bin/env python3
'''
Scrape metadata from an NEC Retro page, e.g. https://necretro.org/List_of_TurboGrafx-CD_(CD-ROM%C2%B2)_games_in_the_United_States
'''
from bs4 import BeautifulSoup
from pathlib import Path
from sys import argv

# main program
if __name__ == "__main__":
    assert len(argv) == 3, "USAGE: %s <games_dir> <necretro_html>" % argv[0]
    games_dir = Path(argv[1])
    if not games_dir.exists():
        games_dir.mkdir()
    with open(argv[2], 'rt') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    for row in soup.find_all('tr'):
        cols = [col.text.strip() for col in row.find_all('td')]
        if len(cols) == 0:
            continue
        name, release_date, rrp, serial = cols
        release_date = release_date.split('[')[0].strip()
        game_dir = games_dir / serial
        if not game_dir.exists():
            game_dir.mkdir()
        for fn, data in [('title.txt',name), ('release_date.txt',release_date), ('serial.txt',serial)]:
            with open(game_dir / fn, 'wt') as f:
                f.write(data.strip() + '\n')
