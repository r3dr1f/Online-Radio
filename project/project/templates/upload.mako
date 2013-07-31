<%inherit file="default.mako" />
<%block name="title">Upload</%block>
<%block name="page_content">
<h2>Nahrávanie pesničiek</h2>
<!--<form method="POST">
    <div class="input-group">
        <label for="email">E-mail</label>
        <input type="email" name="email" id="email" required/>
    </div>
    <div class="input-group">
        <label for="password">Heslo</label>
        <input type="password" name="password" id="password" required/>
    </div>
    <div class="input-group">
        <label for="password_repeat">Heslo znovu</label>
        <input type="password" name="password_repeat" id="password_repeat" required/>
    </div>
    <button type="submit" class="submit-form">Zaregistrovať sa</button>
</form>-->
% if ok == 1:
	<span>Upload OK</span>
% endif
<form action="${request.route_path('upload')}" method="post" accept-charset="utf-8" enctype="multipart/form-data">

	<label for="name">Name</label><br />
    <input id="name" name="name" type="text" value="" /><br /><br />
    <label for="mp3">Mp3</label><br />
    <input id="mp3" name="mp3" type="file" value="" /><br /><br />

    <input type="submit" value="Upload" />
</form>
</%block>
