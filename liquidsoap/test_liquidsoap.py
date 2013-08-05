import unittest
from next_song import generate_next_song

class SimplisticTest(unittest.TestCase):
    
    fname = "test.m3u" # testovaci playlist
    
    def test_if_generated_five_and_init_test_playlist(self):
        fname = "test.m3u" # testovaci playlist
        
        file = open(fname, "w") # writes list with songs to playlist file
        file.write("".join(map(lambda x: str(x), []))) # vytvorime prazdny playlist
        file.close()
        
        generate_next_song("test.m3u")
        try:
            with open(fname) as f:
                songs = f.readlines() 
        except:
            print("Failed to open " + fname)
        #print(len(songs))
        assert(len(songs) == 5)
    
    """
        test, ci sa posunuli dobre riadky playlistu
    """
    """
    def test_on_full_playlist(self):
        
        fname = "test.m3u" # testovaci playlist
        
        try: # nacitame povodne pesnicky
            with open(fname) as f:
                songs_original = f.readlines() 
        except:
            print("Failed to open " + fname)
        
        generate_next_song("test.m3u") # dogenerujeme nahodne
        
        try:    # nacitame novy playlist
            with open(fname) as f:
                songs = f.readlines() 
        except:
            print("Failed to open " + fname)
        for i in range(1,4): # otestujeme, ci sa to posunulo spravne
            assert(songs[i] == songs_original[i + 1])
    """     

if __name__ == '__main__':
    unittest.main()