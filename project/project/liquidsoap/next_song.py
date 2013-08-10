import random
import sys
from project.models.song import Song
from project.models.playlist import Playlist
from project.liquidsoap import _session
from datetime import date


fname = "playlist.m3u"
playlist_length = 5

"""
    roulette wheel selection on the dictionary {song_id:weight}
"""

def roulette_selection(song_weight_table):
    max = sum(song_weight_table.values())
    pick = random.uniform(0, max)
    current = 0
    for key, value in song_weight_table.items():
        current += value
        if current > pick:
            return key 
    

"""
    returns id of next song to play
"""

def pick_next_song():
    songs = _session.query(Song, Song.rating_max * Song.factor_played * Song.factor_age).all()
    x = {song:weight for (song,weight) in songs}
    return roulette_selection(x)

"""
    returns path to next song to play
"""

def path_to_song(song_id):
    return "./songs/" + str(song_id) + ".mp3"

"""
    fills playlist with next 5 files to play
"""

def generate_next_song(fname = fname):
    songs = []
    
    try:
        songs = _session.query(Playlist.song_id).filter(Playlist.play_time == None).order_by("id asc").all()  
        #vyberie to pesnicky, co este neboli prehrate a rovno aj cesty k nim
        songs = [path_to_song(song_id) + "\n" for (song_id,) in songs]
    except:
        print("failed to connect to db")
    finally:
        while (len(songs) < playlist_length): #naplnenie playlistu
            next_song = pick_next_song()
            songs.append(path_to_song(next_song.id) + "\n")
            _session.add(Playlist(next_song,None)) #pridanie songu do databazy bez casu prehrania, kedze este sa len ide prehrat
        _session.commit()
        file = open(fname, "w") # writes list with songs to playlist file
    
        songs = [path_to_song("FAIL") + "\n"] + songs[0:1]; #FAILy su pridane, aby liquidsoap nereloadoval moc skoro
        songs.append(path_to_song("FAIL") + "\n");
        songs.append(path_to_song("FAIL") + "\n");
        file.write("".join(map(lambda x: str(x), songs)))
        file.close()
     
    print("written to file: %s",songs)