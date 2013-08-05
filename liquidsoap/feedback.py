#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
from time import gmtime, strftime
from next_song import generate_next_song
import dbconnect #pripojenie k databaze

con = None

try:
	#pri prepinaci -init sa nepripaja k databaze, chceme len vytvorit playlist s 5 pesnickami
	# -init znamena, ze ideme nainicializovat playlist
	if (sys.argv[1] != "-init"): 
		con = dbconnect.connect()
		cur = con.cursor()
		cur.execute("SELECT * FROM playlist WHERE (song_id = %s AND play_time is NULL) ORDER BY id ASC LIMIT 1;"%(sys.argv[1]))
		id = int(cur.fetchone()[0]) #najskorsie id v playliste, co este nebolo prehrane ideme updatnut, ze uz bolo prehrane
		cur.execute('UPDATE playlist SET play_time = datetime() WHERE (song_id = %s AND play_time is NULL AND id = %s) '%(sys.argv[1],id))
		print ('UPDATE playlist SET play_time = datetime() WHERE (song_id = %s AND play_time = NULL AND id=%s) '%(sys.argv[1],id))
		con.commit()          
    
except:
    print("FAILED TO UPDATE RECORD IN TABLE PLAYLIST")
    
finally:
    
    if con:
        con.close()
    generate_next_song()
