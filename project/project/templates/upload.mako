<%inherit file="default.mako" />
<%block name="title">Upload</%block>
<%block name="page_content">
<h2>Nahrávanie pesničiek</h2>
% if ok == 1:
	<span>Upload OK</span>
% elif error == 'mp3':
	<span>Zvoľte pesničku</span>
% elif error == 'mime':
	<span>Zvoľte pesničku vo formáte mp3</span>
% elif error == 'name':
	<span>Zadajte názov pesničky</span>
% endif
<form action="${request.route_path('upload')}" method="post" accept-charset="utf-8" enctype="multipart/form-data">

	<label for="name">Name</label><br />
    <input id="name" name="name" type="text" value="" /><br /><br />
    <label for="mp3">Mp3</label><br />
    <input id="mp3" name="mp3" type="file" value="" /><br /><br />

    <input type="submit" value="Upload" />
</form>
</%block>
