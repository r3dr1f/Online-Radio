<!DOCTYPE HTML>
<html lang="sk-SK">
<head>
	<meta charset="utf-8">
		<link type="text/css" href="${request.static_path('project:static/skins/jplayer.blue.monday.css')}" rel="stylesheet" />
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery.jplayer.min.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery.jplayer.inspector.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/themeswitcher.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/scripts.js')}"></script>
		<script type="text/javascript">
		    $(document).ready(function(){
      		var stream = {
			title: "ABC Jazz",
			//mp3: "http://listen.radionomy.com/abc-jazz"
			//mp3: "http://127.0.0.1:1234/stream"
			//mp3: "http://tombadoma.dyndns.org:8080/stream"
			mp3: "http://localhost:8000/stream"
			},
			ready = false;

			$("#jquery_jplayer_1").jPlayer({
				ready: function (event) {
				ready = true;
				$(this).jPlayer("setMedia", stream);
				},
				pause: function() {
				$(this).jPlayer("clearMedia");
				},
				error: function(event) {
					if(ready && event.jPlayer.error.type === $.jPlayer.error.URL_NOT_SET) {
					// Setup the media stream again and play it.
					console.log("error");
					$(this).jPlayer("setMedia", stream).jPlayer("play");
					}
				},
				swfPath: "${request.static_path('project:static/js')}",
				supplied: "mp3",
				preload: "none",
				wmode: "window",
				keyEnabled: true
				});
    		});
		</script>
    <link href="${request.static_path('project:static/stylesheets/screen.css')}" media="screen, projection" rel="stylesheet" type="text/css" />
</head>

<body id='museum'>
    <div id="main">
        <div id="header">
            <h1><a href="/">Project</a></h1>
            <div class="login">
            % if request.userid is None:
                <div id="log in">
                    <form class="login-form" action="${request.route_path('login')}" method="POST">
                        <div class="input-group">
                            <label for="email-login">E-mail</label>
                            <input type="email" name="email" id="email-login" required/>
                        </div>
                        <div class="input-group">
                            <label for="password-login">Heslo</label>
                            <input type="password" name="password" id="password-login" required/>    
                        </div>
                        <button type="submit" class="submit-form">Prihlásiť sa</button>
                        <a class="register-button" href="${request.route_path('register')}">Zaregistrovať sa</a>
                        <div class="recovery-password">
                        <a href="${request.route_path('beg_for_recovery')}" >Zabudol som heslo</a>
                        </div>
                    </form>
                </div>
            % else:
                <form action="${request.route_path('logout')}" method="POST">
                    <button type="submit" class="signout-button">Odhlásiť ${request.user.email}</button>
                </form>
            % endif
            </div>
        </div>
        <div id='content'>
            <%block name="page_content">${content | n}</%block>
        </div>
    </div>
</body>
</html>
