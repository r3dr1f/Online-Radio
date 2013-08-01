import random
import dbconnect

fname = "playlist.m3u"
playlist_length = 5

"""
    returns path to next song to play
"""
def pick_next_song():
    con = dbconnect.connect()
    query = con.cursor()
    query.execute("SELECT * FROM song ORDER BY RANDOM() LIMIT 1;")
    
    return "./songs/" + str(query.fetchone()[0]) + ".mp3" #[0] akoze prvy stlpec, cize id

"""
    fills playlist with next 5 files to play
"""
def generate_next_song(fname = fname):
    print(fname)
    songs = []
    try:
        with open(fname) as f:
            songs = f.readlines() 
            songs.pop(0) # vrchnu pesnicku zmazeme (to je ta, co sa aktualne prehrava)
    except:
        print("Failed to open " + fname)
    while (len(songs) < playlist_length): 
        songs.append(pick_next_song() + "\n")
        
    file = open(fname, "w") # writes list with songs to playlist file
    file.write("".join(map(lambda x: str(x), songs)))
    file.close()
    print(songs)