import random
import dbconnect
import sys

fname = "playlist.m3u"
playlist_length = 5


"""
    returns id of next song to play
"""

def pick_next_song():
    con = dbconnect.connect()
    query = con.cursor()
    query.execute("SELECT * FROM song ORDER BY RANDOM() LIMIT 1;")
    
    return int(query.fetchone()[0]) #[0] akoze prvy stlpec, cize id


"""
    returns path to next song to play
"""

def path_to_song(song_id):
    return "./songs/" + str(song_id) + ".mp3"

"""
    fills playlist with next 5 files to play
"""
def generate_next_song(fname = fname):
    print(fname)
    songs = []
    try:
        #with open(fname) as f:
            #songs = f.readlines() 
        #songs.pop(0) # vrchnu pesnicku zmazeme (to je ta, co sa aktualne prehrava)
        con = dbconnect.connect()
        cur = con.cursor()
        cur.execute('SELECT song_id FROM playlist WHERE play_time is NULL ORDER BY id ASC;')
        #vyberie to pesnicky, co este neboli prehrate a rovno aj cesty k nim
        songs = [path_to_song(song_id) + "\n" for (song_id,) in cur.fetchall()]     
    except:
        print("Failed to connect to database")
    while (len(songs) < playlist_length): 
        next_song_id = pick_next_song()
        songs.append(path_to_song(next_song_id) + "\n")
        #insertnutie do databazy playlist pasnicky, co sa ide hrat
        con = dbconnect.connect()
        cur = con.cursor()
        cur.execute('INSERT INTO playlist (song_id,play_time) VALUES (%s,NULL)'%(next_song_id))
        #play_time NULL znamena, ze pesnicka este nebola prehrana, ale chysta sa prehrat
        con.commit()
        print("generated next song")
        
    file = open(fname, "w") # writes list with songs to playlist file
    file.write("".join(map(lambda x: str(x), songs)))
    file.close()
    print(songs)
    
generate_next_song()