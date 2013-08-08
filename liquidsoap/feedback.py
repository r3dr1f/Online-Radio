#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
from time import gmtime, strftime
from next_song import generate_next_song
import dbconnect #pripojenie k databaze

con = None

def create_empty_playlist():
	file = open("playlist.m3u", "w") # writes list with songs to playlist file
	file.write("")
	file.close()

print(sys.argv[1])

try:
	#pri prepinaci -init sa nepripaja k databaze, chceme len vytvorit playlist s 5 pesnickami
	# -init znamena, ze ideme nainicializovat playlist
	if (sys.argv[1] != "-init"): 
		con = dbconnect.connect()
		cur = con.cursor()
		#print("SELECT id FROM playlist WHERE (song_id = %s AND play_time is NULL) ORDER BY id ASC LIMIT 1;"%(sys.argv[1]))
		cur.execute("SELECT id FROM playlist WHERE (song_id = %s AND play_time is NULL) ORDER BY id ASC LIMIT 1;"%(sys.argv[1]))
		id = int(cur.fetchone()[0]) #najskorsie id v playliste, co este nebolo prehrane ideme updatnut, ze uz bolo prehrane
		#print ('UPDATE playlist SET play_time = datetime() WHERE (song_id = %s AND play_time = NULL AND id=%s) '%(sys.argv[1],id))
		cur.execute('UPDATE playlist SET play_time = datetime() WHERE (song_id = %s AND play_time is NULL AND id = %s) '%(sys.argv[1],id))
		con.commit()
	else:
		create_empty_playlist()          
    
except:
    #print("FAILED TO UPDATE RECORD IN TABLE PLAYLIST",sys.exc_info()[0])
    pass
   
finally:
    
    if con:
        con.close()
    generate_next_song()
