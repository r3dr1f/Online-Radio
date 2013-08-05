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
		#print('INSERT INTO playlist (song_id,play_time) VALUES (%s,datetime())'%(sys.argv[1]))
		cur.execute('INSERT INTO playlist (song_id,play_time) VALUES (%s,datetime())'%(sys.argv[1]))
		con.commit()          
    
except:
    print("FAILED TO ADD RECORD TO TABLE PLAYLIST")
    
finally:
    
    if con:
        con.close()
    generate_next_song()
    print("generated next song")
