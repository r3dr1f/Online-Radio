<!DOCTYPE HTML>
<html lang="sk-SK" xmlns:fb="http://ogp.me/ns/fb#">
<head>
	<meta charset="utf-8">
		<link href="${request.static_path('project:static/stylesheets/screen.css')}" media="screen, projection" rel="stylesheet" type="text/css" />
		<link type="text/css" href="${request.static_path('project:static/stylesheets/jquery.Jcrop.min.css')}" rel="stylesheet" />
		<link type="text/css" href="${request.static_path('project:static/skins/jplayer.blue.monday.css')}" rel="stylesheet" />
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery-1.10.2.min.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery.form.min.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery.jplayer.min.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery.jplayer.inspector.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/themeswitcher.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/underscore-min.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery.Jcrop.min.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/scripts.js')}"></script>
		<script type="text/javascript">
		    $(document).ready(function(){
      		var stream = {
			title: "ABC Jazz",
			//mp3: "http://listen.radionomy.com/abc-jazz"
			//mp3: "http://127.0.0.1:1234/stream"
			//mp3: "http://tombadoma.dyndns.org:8080/stream"
			mp3: "http://localhost:8080/stream"
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
					$(this).jPlayer("setMedia", stream).jPlayer("play");
					}
				},
				swfPath: "${request.static_path('project:static/js')}",
				supplied: "mp3",
				preload: "none",
				wmode: "window",
				keyEnabled: false
				});
    		});
		</script>
    <!-- Facebook Share meta tags -->
    <meta property="og:title" content="Rádio"/>
    <meta property="og:site_name" content="Naše rádio"/>
    <meta property="og:url" content="http://naseradio.sk"/>
</head>

<body id='museum'>

<div id="jquery_jplayer_1" class="jp-jplayer"></div>
  <div id="jp_container_1" class="jp-audio">
    <div class="jp-type-single">
      <div class="jp-gui jp-interface">
      	<div id="logo">LOGO</div>
        <ul class="jp-controls">
          <li><a href="javascript:;" class="jp-play" tabindex="1">play</a></li>
          <li><a href="javascript:;" class="jp-pause" tabindex="1">stop</a></li>
          <li><a href="javascript:;" class="jp-mute" tabindex="1" title="mute">mute</a></li>
          <li><a href="javascript:;" class="jp-unmute" tabindex="1" title="unmute">unmute</a></li>
          <li><div class="jp-volume-bar"><div class="jp-volume-bar-value"></div></div></li>
          <!--<li><a href="javascript:;" class="jp-volume-max" tabindex="1" title="max volume">max volume</a></li>-->
        </ul>
        <div class="jp-title">
          		<a href="#">&nbsp;</a>
      	</div>
      	<div id="search-form">
        	<label for="search"></label>
        	<input type="text" size="30" name="search" id="search" value="Hľadaj" />
        </div>
        <div id="login-button">
        	<a href="#">Prihlásiť</a>
        	<div id="login-content">
        		
        	</div>
        </div>
      </div>
      
      <!--<div class="jp-no-solution">
        <span>Update Required</span>
        To play the media you will need to either update your browser to a recent version or update your <a href="http://get.adobe.com/flashplayer/" target="_blank">Flash plugin</a>.
      </div>-->
    </div>
  </div>

<div id="fb-root"></div>
<script>
  window.fbAsyncInit = function() {
    // init the FB JS SDK
    FB.init({
      appId      : '416080778513149',                        // App ID from the app dashboard
      channelUrl : '${request.static_path('project:static/channel.html')}', // Channel file for x-domain comms
      status     : true,                                 // Check Facebook Login status
      xfbml      : true,                                  // Look for social plugins on the page
      cookie	 : true,
      oauth		 : true      
    });

    // Additional initialization code such as adding Event Listeners goes here
  };

  // Load the SDK asynchronously
  (function(d, s, id){
     var js, fjs = d.getElementsByTagName(s)[0];
     if (d.getElementById(id)) {return;}
     js = d.createElement(s); js.id = id;
     js.src = "http://connect.facebook.net/en_US/all.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));
   


   
   
</script> 
    <div id="main">
        <div id="header">
        	<div class="fb-like" data-href="http://www.facebook.com/pages/Test/487965897961635" data-width="450" data-show-faces="true" data-send="false"></div>
        	<div id="image-upload"></div>
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
                        <a class="register-button" id="fb-login" href="#">Prihlásiť sa pomocou facebooku</a>
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
        <div id="search-info">
        </div>
        <div id='content'>
            <%block name="page_content">${content | n}</%block>
        </div>
    </div>
</body>
</html>
