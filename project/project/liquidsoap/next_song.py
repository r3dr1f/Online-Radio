"""
    next_song.py 
        - generates next song to play and adds it to database playlist
"""

import random
import sys
from project.models.song import Song
from project.models.playlist import Playlist
from project.liquidsoap import _session
import datetime


fname = "playlist.m3u"
playlist_length = 5

"""
    sets "queued" column for currently added song to playlist to True
"""

def commit_playing_song(song_id):
    cur_song = _session.query(Playlist).filter(Playlist.song_id == song_id, Playlist.queued == False).order_by("id asc").first()
    if (cur_song != None):
        cur_song.queued = True
        _session.add(cur_song)
        _session.commit()
    else:
        sys.stderr.write("commit_playing_song: INVALID SONG COMMITED!\n")   

"""
    roulette wheel selection on the dictionary {song:weight}
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
        songs = _session.query(Playlist.song_id).filter(Playlist.queued == False).order_by("id asc").all() 
        songs = [song_id for (song_id,) in songs]
    except:
        print("failed to connect to db")
    finally:
        while (len(songs) < playlist_length): #naplnenie playlistu
            next_song = pick_next_song()
            songs.append(next_song.id)
            _session.add(Playlist(next_song,None,False)) #pridanie songu do databazy bez casu prehrania, kedze este sa len ide prehrat
        _session.commit()
        
        print(path_to_song(songs[0]))
        commit_playing_song(songs[0]) #nastavime danemu songu, ze je uz zaradeny vo fronte, kedze sme ho poslali printom do liquidsoapu  
    
generate_next_song()