#!/usr/bin/liquidsoap 
# Log dir 
set("log.file.path","/tmp/basic-radio.log")

def my_request_function() = 
  # Get the first line of my external process
  result =
    list.hd(
      get_process_lines("python3.3 -c 'import next_song; next_song.generate_next_song()'"))
  # Create and return a request using this result
  print("#{result}")
  request.create(result)
end

def apply_metadata(m) =
  title = m["filename"]
  print("Now playing: #{title}")
  
  filename = string.split(separator="/",title) # rozdelime cestu po lomitkach
  filename = list.nth(list.rev(filename),0) # vezmeme meno suboru
  filename = list.nth(string.split(separator="\.",filename),0) # odpojime koncovku .mp3

  command = "python3.3 -c 'import feedback; feedback.run()' " ^ filename
  system(command)
end

#set queued but not played songs to unqueued (can happen if liquidsoap was suddenly closed)
system("python3.3 -c 'import feedback; feedback.initialize_playlist()' ")

# Create the source
s = request.dynamic(my_request_function)
s = on_track(apply_metadata,s)

output.icecast(%mp3, host = "localhost", port = 8080, password = "baldur", mount = "stream", s, fallible=true)