${song_name.name}

Playlist:<br>
% for song in playlist:
	${song.song.name}<br>
% endfor