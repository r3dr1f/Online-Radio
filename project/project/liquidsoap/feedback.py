"""
	feedback.py 
		- this file is called from script.liq to add currently played song to database table playlist
"""

import sys
from project.models.playlist import Playlist
from project.liquidsoap import _session
from project.models.song import Song
import datetime


def update_factor_played():
	songs = _session.query(Song).all()
	#print(songs)
	for song in songs:
		song.current_rating = (9 * song.current_rating + song.rating_max * song.factor_age) / 10
		_session.add(song)
	_session.commit()
	
	songs_to_be_played = _session.query(Song).join(Playlist).filter(Playlist.play_time == None).all()
	#print(songs_to_be_played)
	for song in songs_to_be_played:
		song.current_rating = 0
		_session.add(song)
	_session.commit()


#-init means cleaning database playlist from queued but not played songs
if (sys.argv[1] == "-init"):
	queued_but_not_played_songs = _session.query(Playlist).filter(Playlist.play_time == None, Playlist.queued == True).order_by("id asc").all()
	for song in queued_but_not_played_songs:
		song.queued = False
		_session.add(song)
	_session.commit()
	sys.exit(0)

try:
	#pesnicke, co sa prave prehrava nastavime cas, kedy sa zacala prehravat, cize aktualny cas
	cur_song = _session.query(Playlist).filter(Playlist.song_id == sys.argv[1], Playlist.play_time == None).order_by("id asc").first()
	cur_song.play_time = datetime.datetime.now()
	_session.add(cur_song)
	_session.commit()    
except:
    print("FAILED TO UPDATE RECORD IN TABLE PLAYLIST",sys.exc_info()[0])
update_factor_played()