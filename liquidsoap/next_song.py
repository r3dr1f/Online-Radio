import random

fname = "playlist.m3u"

"""
    returns path to next song to play
"""
def pick_next_song():
    return "./" + str(random.randrange(1,4)) + ".mp3"

"""
    fills playlist with next 5 files to play
"""
def generate_next_song():
    songs = []
    try:
        with open(fname) as f:
            songs = f.readlines() 
            songs.pop(0) # vrchnu pesnicku zmazeme (to je ta, co sa aktualne prehrava)
    except:
        print("Failed to open " + fname)
    while (len(songs) < 5):
        songs.append(pick_next_song() + "\n")
        
    file = open(fname, "w") # writes list with songs to playlist file
    file.write("".join(map(lambda x: str(x), songs)))
    file.close()
    print(songs)