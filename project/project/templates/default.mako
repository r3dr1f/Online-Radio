<!DOCTYPE HTML>
<html lang="sk-SK" xmlns:fb="http://ogp.me/ns/fb#">
<head>
	<meta charset="utf-8">
		<link href="${request.static_path('project:static/stylesheets/screen.css')}" media="screen and (min-width: 1100px), projection and (min-width: 1100px)" rel="stylesheet" type="text/css" />
		<link href="${request.static_path('project:static/stylesheets/screen_small.css')}" media="screen and (max-width: 1099px), projection and (max-width: 1099px)" rel="stylesheet" type="text/css" />
		<link type="text/css" href="${request.static_path('project:static/stylesheets/jquery.Jcrop.min.css')}" rel="stylesheet" />
		<link type="text/css" href="${request.static_path('project:static/skins/jplayer.blue.monday.css')}" rel="stylesheet" media="screen and (min-width: 1100px), projection and (min-width: 1100px)"/>
		<link type="text/css" href="${request.static_path('project:static/skins/jplayer.blue.monday_small.css')}" rel="stylesheet" media="screen and (max-width: 1099px), projection and (max-width: 1099px)""/>
		
		
		<link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Comfortaa&subset=latin,latin-ext">
		
		<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.1/jquery.min.js"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery-ui-1.10.3-effects.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery.jplayer.min.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery.jplayer.inspector.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery.form.min.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/themeswitcher.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/underscore-min.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/jquery.Jcrop.min.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/components.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/scripts.js')}"></script>
		<script type="text/javascript" src="${request.static_path('project:static/js/main.js')}"></script>
		<script type="text/javascript">
			
			$(document).ready(function(){
		    
		    
		    	/*tuto riesime spravne resizovanie toolbaru a posuvanie pri horizontalnom scrolle*/
		    	$("#jp_container_1").css("margin-left", -$(document).scrollLeft());
				$("#jp_container_1").css("width",Math.max($(document).width(),$("body").width() ));
		    
		    	$(window).on("scroll resize", function() {
					$("#jp_container_1").css("margin-left", -$(document).scrollLeft());
					$("#jp_container_1").css("width",Math.max($(document).width(),$("body").width() ));
				});
			});
		</script>
		
		
    <!-- Facebook Share meta tags -->
    <meta property="og:title" content="Rádio"/>
    <meta property="og:site_name" content="Naše rádio"/>
    <meta property="og:url" content="http://naseradio.sk"/>
</head>

<body>

<div id="jquery_jplayer_1" class="jp-jplayer"></div>
  <div id="jp_container_1" class="jp-audio">
    <div id="logo"> <img src = "../static/images/3sk_logo_orange_mini.png" style="height: 2.5em;" > </div>
    <div class="jp-type-single">
      <div class="jp-gui jp-interface">
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
      	
      	<div id="my-account">
        	<a href="#"><img src="../static/images/profile.png" width="32" height="32" class="playlist-icon"></a>
        	<div id="login-content">
        	</div>
        </div>
      	
      	<div id="search-form">
        	<label for="search"></label>
        	<input type="text" size="30" name="search" id="search" value="Hľadaj" />
        </div>
      </div>
      
      <!--<div class="jp-no-solution">
        <span>Update Required</span>
        To play the media you will need to either update your browser to a recent version or update your <a href="http://get.adobe.com/flashplayer/" target="_blank">Flash plugin</a>.
      </div>-->
    </div>
  </div>
  
<div class="playlist">
 	<table id="playlist"></table>
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
     js.src = "//connect.facebook.net/en_US/all.js";
     fjs.parentNode.insertBefore(js, fjs);
   }(document, 'script', 'facebook-jssdk'));
   


   
   
</script> 
    <div id="main">
        <div id="header">
        	<div class="fb-like" data-href="http://www.facebook.com/pages/Test/487965897961635" data-width="450" data-show-faces="true" data-send="false"></div>
        	<!--<div id="image-upload"></div>-->
        </div>
        <div id="search-info">
        </div>
        <div id='content'>
            <%block name="page_content">${content | n}</%block>
        </div>
    </div>
</body>
</html>
