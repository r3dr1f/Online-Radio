#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from project.liquidsoap.next_song import generate_next_song
from project.models.playlist import Playlist
from project.liquidsoap import _session
import datetime

con = None

def create_empty_playlist():
	file = open("playlist.m3u", "w") # writes list with songs to playlist file
	file.write("")
	file.close()

try:
	#pri prepinaci -init sa nepripaja k databaze, chceme len vytvorit playlist s 5 pesnickami
	# -init znamena, ze ideme nainicializovat playlist	
	if (sys.argv[1] != "-init"): 
		#pesnicke, co sa prave prehrava nastavime cas, kedy sa zacala prehravat, cize aktualny cas
		cur_song = _session.query(Playlist).filter(Playlist.song_id == sys.argv[1], Playlist.play_time == None).order_by("id asc").first()
		cur_song.play_time = datetime.datetime.now()
		_session.add(cur_song)
		_session.commit()
	else:
		create_empty_playlist()          
    
except:
    print("FAILED TO UPDATE RECORD IN TABLE PLAYLIST",sys.exc_info()[0])
   
finally:
    generate_next_song()
