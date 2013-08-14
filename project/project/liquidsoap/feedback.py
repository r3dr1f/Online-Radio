"""
	feedback.py 
		- this file is called from script.liq to add currently played song to database table playlist
"""

import sys
from project.models.playlist import Playlist
from project.liquidsoap import _session
from project.models.song import Song
import datetime

#cleans database playlist from queued but not played songs
def initialize_playlist():
	queued_but_not_played_songs = _session.query(Playlist).filter(Playlist.play_time == None, Playlist.queued == True).order_by("id asc").all()
	for song in queued_but_not_played_songs:
		song.queued = False
		_session.add(song)
	_session.commit()
	sys.exit(0)

def run():	
	try:
		#pesnicke, co sa prave prehrava nastavime cas, kedy sa zacala prehravat, cize aktualny cas
		cur_song = _session.query(Playlist).filter(Playlist.song_id == sys.argv[1], Playlist.play_time == None).order_by("id asc").first()
		cur_song.play_time = datetime.datetime.now()
		_session.add(cur_song)
		_session.commit()    
	except:
		print("FAILED TO UPDATE RECORD IN TABLE PLAYLIST",sys.exc_info()[0])
	#update_current_rating()