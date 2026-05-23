#! /usr/bin/env python3
'''
Scrape metadata from HTML of an NEC Retro page, e.g. https://necretro.org/List_of_TurboGrafx-CD_(CD-ROM%C2%B2)_games_in_the_United_States
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
        if 'arcade_cdrom2' in argv[2]:
            cd_format = 'Arcade CD-ROM²'
        elif 'super_cdrom2' in argv[2]:
            cd_format = 'Super CD-ROM²'
        elif 'cdrom2' in argv[2]:
            cd_format = 'CD-ROM²'
        else:
            cd_format = None
        if '_japan' in argv[2]:
            region = 'NTSC-J'
        elif '_usa' in argv[2]:
            region = 'NTSC-U'
        else:
            region = None
        if not game_dir.exists():
            game_dir.mkdir()
        for fn, data in [
            ('title.txt', name),
            ('release_date.txt', release_date),
            ('serial.txt', serial),
            ('cd_format.txt', cd_format),
            ('region.txt', region),
        ]:
            if data is not None:
                with open(game_dir / fn, 'wt') as f:
                    f.write(data.strip() + '\n')
