# This function is called when
# a new metadata block is passed in
# the stream.
def apply_metadata(m) =
  title = m["filename"]
  artist = m["artist"]
  print("Now playing: #{title} by #{artist}")
  
  filename = string.split(separator="/",title) # rozdelime cestu po lomitkach
  filename = list.nth(list.rev(filename),0) # vezmeme meno suboru
  filename = list.nth(string.split(separator="\.",filename),0) # odpojime koncovku .mp3
  
  command = "python3 feedback.py " ^ filename
  system(command)

end

#!/usr/bin/liquidsoap 
# Log dir 
set("log.file.path","/tmp/basic-radio.log")
# Music 
myplaylist = playlist(mode="normal","./playlist.m3u",reload_mode="rounds",reload=1)

myplaylist = on_metadata(apply_metadata,myplaylist)

# Stream it out 
output.icecast(%mp3, host = "localhost", port = 8080, password = "baldur", mount = "stream", myplaylist, fallible=true)


