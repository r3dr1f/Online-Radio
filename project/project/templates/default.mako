<!DOCTYPE HTML>
<html lang="sk-SK">
<head>
	<meta charset="utf-8">
		<link type="text/css" href="${request.static_path('project:static/skins/jplayer.blue.monday.css')}" rel="stylesheet" />
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery.jplayer.min.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery.jplayer.inspector.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/themeswitcher.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/underscore-min.js')}"></script>
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
    <link href="${request.static_path('project:static/stylesheets/screen.css')}" media="screen, projection" rel="stylesheet" type="text/css" />
</head>

<body id='museum'>
<div id="fb-root"></div>
<script>
  window.fbAsyncInit = function() {
    // init the FB JS SDK
    FB.init({
      appId      : '416080778513149',                        // App ID from the app dashboard
      channelUrl : '${request.static_path('project:static/channel.html')}', // Channel file for x-domain comms
      status     : true,                                 // Check Facebook Login status
      xfbml      : true,                                  // Look for social plugins on the page
      oauth      : true
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
   
   
  $(document).ready(function(){
   
});


   
</script> 
    <div id="main">
        <div id="header">
            <h1><a href="#">Project</a></h1>
            <div class="login">
            </div>
        <div>
        	<label for="search"></label>
        	<input type="text" size="30" name="search" id="search">
        	<input type="submit" name="search-it" id="search-it" value="Vyhladat">
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
