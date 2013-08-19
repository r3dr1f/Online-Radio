"""
    next_song.py 
        - generates next song to play and adds it to database playlist
"""

import random
import sys
from project.models.song import Song
from project.models.playlist import Playlist
from project.models.request import Request
from project.liquidsoap import _session
from datetime import datetime
from datetime import timedelta

playlist_length = 5

"""
    deletes all requests to play for song
"""

def delete_request_to_play(song):
    requests = _session.query(Request).filter(Request.song == song).all()
    for request in requests:
        _session.delete(request)
    _session.commit()

"""
    determine_factor_age - returns number in the interval [0.5,1] describing the age of the song
"""

def determine_factor_age(song): # po tyzdnoch bude factor_age klesat o 0.05, az dosiahne 0.5 
    t1 = song.date_added
    t2 = datetime.now()

    tdelta = t2 - t1 # actually a datetime.timedelta object
    #print(t1," ",tdelta.days)
    res = max(0.5, 1.0 - int(tdelta.days / 7) * 0.05)
    return res

def update_factor_age():
    songs = _session.query(Song).all()
    for song in songs:
        song.factor_age = determine_factor_age(song)
        _session.add(song)
    _session.commit()

"""
    update_current_song - updates current rating of all the sogs
"""

def update_current_rating():
    try:
        songs = _session.query(Song).all()
        for song in songs:
            if (song.current_rating < song.rating_max): #keby requesty sposobili, ze current_rating bude vacsi ako rating_max
                song.current_rating = (9 * song.current_rating + song.rating_max * song.factor_age) / 10
            _session.add(song)
        _session.commit()
    except:
        print("Failed to update song ratings")
        
    #vynulujeme rating songom v playliste, co sa este len chystaju prehrat, ale vieme, ze sa prehraju
    try:
        songs_to_be_played = _session.query(Song).join(Playlist).filter(Playlist.play_time == None).all()
        #print(songs_to_be_played)
        for song in songs_to_be_played:
            delete_request_to_play(song)
            song.current_rating = 0
            _session.add(song)
        _session.commit()
    except:
        print("failed to set song ratings to 0")
    finally:
        update_factor_age()

"""
    sets "queued" column for currently added song to playlist to True
"""

def commit_queued_song(song_id):
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
    songs = _session.query(Song, Song.current_rating).all()
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

def generate_next_song():
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
            update_current_rating()
        _session.commit()
        
        commit_queued_song(songs[0]) #nastavime danemu songu, ze je uz zaradeny vo fronte, kedze sme ho poslali printom do liquidsoapu 
        print(path_to_song(songs[0])) 