from downloader import *

def main():
    song_name = "blood oceans pharaoh"
    page_num = 1
    songs_list = search_song(song_name, page_num)

    for song_id, song in enumerate(songs_list):
        print(song_id, song[0])
    name = download_song(songs_list[0][0], songs_list[0][1])
    print(name)

if __name__ == '__main__':
    main()
