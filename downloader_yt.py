from yt_dlp import YoutubeDL
from ytmusicapi import YTMusic

import utils


def search_song(song_name, page_num=1):
    songs_list = []
    with YTMusic() as ytmusic:
        search_results = ytmusic.search(song_name, filter="songs")
    for res in search_results:
        if len(songs_list) >= 10:
            break
        if res["resultType"] == "song":
            title = res["title"]
            artist = ", ".join([dic['name'] for dic in res["artists"] if 'name' in dic])
            duration = res["duration"]
            song_id = res["videoId"]
            songs_list.append({
                'title': title,
                'artist': artist,
                'duration': duration,
                'id': song_id,
            })
    return songs_list


def download_song(song_name, song_id):
    url = "https://music.youtube.com/watch?v={}".format(song_id)
    filename = "{}.m4a".format(utils.slugify(song_name))
    directory = './songs'
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'paths': {
            'home': directory
        },
        'outtmpl': {
            'default': filename
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)

    return filename


def download_sond_by_url(url):
    utils.cleanup()
    directory = './songs'
    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'paths': {
            'home': directory
        },
        'outtmpl': {
            'default': "def.m4a"
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }
    with YoutubeDL(ydl_opts) as ydl:
        data = ydl.extract_info(url, download=False)
        info = ydl.sanitize_info(data)
        filename = "{}.m4a".format(utils.slugify(info['title']))
        ydl_opts['outtmpl']['default'] = filename
        ydl.download(url)
    return [info['title'], filename]
