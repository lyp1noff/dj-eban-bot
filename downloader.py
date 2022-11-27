import requests
from bs4 import BeautifulSoup

import utils


def search_song(song_name, page_num):
    search_url = "https://downloadmusicvk.ru/audio/search?q={}&page={}".format(song_name, page_num)
    r = requests.get(search_url)

    soup = BeautifulSoup(r.text, "html.parser")
    songs_list_raw = soup.findAll('div', class_='row audio vcenter')
    songs_list = []
    for data in songs_list_raw:
        if data.find('a') is not None:
            song_name_raw = data.text
            song_name_full = song_name_raw.replace("\n", "")
            title = song_name_full[song_name_full.find(' - ') + 3:song_name_full.find('  ')]
            artist = song_name_full[:song_name_full.find(' - ')]
            duration = song_name_full[song_name_full.find('  ') + 3:-1]

            data = str(data)
            song_id = data[data.find('data-model="') + 12:data.find('">')]

            songs_list.append({
                'title': title,
                'artist': artist,
                'duration': duration,
                'id': song_id,
            })
    return songs_list


def download_song(song_name, song_id):
    utils.cleanup()
    r = requests.get(
        "https://downloadmusicvk.ru/audio/play?data={}".format(song_id))
    song_name_full = song_name[:song_name.find("  ")]
    filename = "{}.mp3".format(utils.slugify(song_name_full))
    with open("songs/{}".format(filename), 'wb') as f:
        f.write(r.content)

    return filename
