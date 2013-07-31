#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
from time import gmtime, strftime
from next_song import generate_next_song

con = None

try:
    con = lite.connect('../project/project.sqlite')
    
    print(sys.argv)
    cur = con.cursor()
    print('INSERT INTO playlist (song_id,play_time) VALUES (%s,datetime())'%(sys.argv[1]))
    cur.execute('INSERT INTO playlist (song_id,play_time) VALUES (%s,datetime())'%(sys.argv[1]))
    con.commit()          
    
except:
    print("FAILED TO ADD RECORD TO TABLE PLAYLIST")
    
finally:
    
    if con:
        con.close()
    generate_next_song()
    print("generated next 5 songs")