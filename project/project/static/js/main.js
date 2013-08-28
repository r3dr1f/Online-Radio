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
	

	$("body").on("click", ".signout-button", function(event){
		event.preventDefault();
		$.ajax({
	  	url: "/logout",
	  	type: "post",
	  	dataType: "json",
	  	success: function(data){
	  		console.log(data);
	  		if(typeof component !== 'undefined')
	  			component.user_login(data.user);
	  		var loginTemplateData = {
						user: data.user
					};
	  		$('#login-content').html(loginTemplate(loginTemplateData));
	  	}
	  });
		return false;
	});
	
	$("body").on("click", "#login", function(event){
		event.preventDefault();
		$.ajax({
	  	url: "/login",
	  	type: "post",
	  	dataType: "json",
	  	data: {email: $('#email-login').val(), password: $('#password-login').val()},
	  	success: function(data){
	  		var loginTemplateData = {
						user: data.user
					};
	  		$('#login-content').html(loginTemplate(loginTemplateData));
	  	}
	  });
		return false;
	});
	
	$("body").on("click", "#register", function(event){
		event.preventDefault();
		$.ajax({
	  	url: "/registracia",
	  	type: "get",
	  	dataType: "json",
	  	success: function(data){
	  		console.log(data);
	  		var loginTemplateData = {
						register: data.register
					};
	  		$('#login-content').html(loginTemplate(loginTemplateData));
	  	}
	  });
		return false;
	});
	
	$("body").on("click", "#register-submit", function(event){
		event.preventDefault();
		var role = "";
		if($('#role').is(':checked'))
			role = 1
		else
			role = 0;
		$.ajax({
	  	url: "/registracia",
	  	type: "post",
	  	dataType: "json",
	  	data: {email: $('#email').val(),
	  	 	   password: $('#password').val(), 
	  	 	   password_repeat: $('#password_repeat').val(), 
	  	 	   role: role, 
	  	 	   interpret_name: $('#interpret_name').val()},
	  	success: function(data){
	  		console.log(data);
	  		var loginTemplateData = {
						register_success: data.register_success
					};
	  		$('#login-content').html(loginTemplate(loginTemplateData));
	  	}
	  });
		return false;
	});
	
	$('body').on("click", ".trigger > input", function(event){
		if($('.trigger > input').is(':checked')){
			$('.trigger > input').attr('checked','checked');
			$('.default_hide').slideToggle("fast");	
		} else {
			$('.trigger > input').removeAttr('checked');
		}
	});
	
	$("body").on("click", "a.info-interpret", function(event){
	  event.preventDefault();
	  var interpret_id = $(this).attr("href").split("/");
	  interpret_id = interpret_id.slice(-1)[0];
  	  component = new Interpret_info(interpret_id);
  	  component.enter($('.song-info'));
	  return false;
	});
	
	$("body").on("click", "a.info-song, .jp-title > a", function(event){
	  event.preventDefault();
	  var song_id = $(this).attr("href").split("/");
  	  song_id = song_id.slice(-1)[0];
  	  component = new Song_info(song_id);
  	  component.enter($('.song-info'));
	  return false;
	});
	
	$("#search").keypress(function(event){
		if(event.which == 13) {
			if(typeof component !== 'undefined'){
		  		component.exit();
		  	}
	        component = new Search_info($("#search").val());
	        component.enter($('.song-info'));
	  	}
	});

//************************************** Custom handlers **************************************************//
	$('.song-info').on('interpret-info-request', function(event, id) {
		event.preventDefault();
	  	if(typeof component !== 'undefined')
	  		component.exit();
	  	component = new Interpret_info(id);
	  	component.enter($('.song-info'));
	})

	$('.song-info').on('song-info-request', function(event, id) {
  	  	event.preventDefault();
  	  	if(typeof component !== 'undefined')
  	  		component.exit();
  	  	component = new Song_info(id);
  	  	component.enter($('.song-info'));
  	});
	
	$("body").on("rate-info-request", function(event, id, rating){
	    event.preventDefault();
	    if(typeof component !== 'undefined')
	   		component.exit();
	    component = new Rating_info(id, rating);
	    component.enter($('.song-info'));
	});
	
	$("body").on("click", ".request-to-play", function(event){
		event.preventDefault();
		var song_id = $(this).attr("href").split("/");
	  	song_id = song_id.slice(-1)[0];
		if(typeof component !== 'undefined')
			component.exit();
		component = new Request_info(song_id);
		component.enter($('.song-info'));
	});
	
	$("#search").focus(function() {
	    if ($(this).val() == "Hľadaj") {
	       $(this).val("");
	    }
	  });
	  
	$("#search").blur(function() {
	    if ($(this).val() == "") {
	      $(this).val("Hľadaj");
	    }
	});
	
	$("body").on("click", ".add-comment", function(event){
		event.preventDefault();
		$("#comment-input").show();
		return false;
	});
	
	$("body").on("keypress", "#comment-input", function(event){
		if(event.which == 13) {
			event.preventDefault();
	        if ($(this).val() != "") {
		        component = new Comments_info($("#song-id").val(), $("#comment-input").val());
		        component.enter($('#song-comments'));
	        }
	    }
	});
	
	$("body").on("click", "#fb-login", function(event){
	   			event.preventDefault();
	            FB.login(
	                function(response){
	                    if (response.authResponse){
	                        FB.api
	                        (
	                            "/me",
	                            function( response )
	                            {
	                                $('#fb-name').val(response.name);
	                                $('#email').val(response.email);
	                                //document.getElementById("obrazok").src = "http://graph.facebook.com/" + response.id + "/picture";
	                                $.ajax({
									  	url: "/login_fb",
									  	type: "post",
									  	dataType: "json",
									  	data: {uuid: response.id, email: response.email},
									  	success: function(data){
									  			console.log(data.user);
												if(typeof component !== 'undefined'){
													component.user_login(data.user.id);
												}
												var templateData = {
													user : data.user
												}
												$('#login-content').html(loginTemplate(templateData));								  		
									  		}
									});
	                            }
	                        )
	                    }
	                }, {scope: 'email'}
	            );
	            return false;
	});
	
	var loginTemplateData = {};
	$('#login-content').html(loginTemplate(loginTemplateData));
	
	
	$("#my-account > a").click(function(e) {
		e.preventDefault();
		$("#log-in").slideToggle('slow');
		return false;
	});
	
	$("#login-button > a").blur(function() {
		$("#login-content").hide();
	});

	function showResponse(responseText, statusText, xhr, $form)  {
	var src = responseText.image.user_id + "/" + responseText.image.name; 
    $("#jcrop-image").attr("src", "/static/tmp/" + src);
    $("#preview").attr("src", "/static/tmp/" + src);
    $("#jcrop-image").show();
    $("#crop-src").val(src);
    
    $('#jcrop-image').Jcrop({
		onChange: showPreview,
		onSelect: showPreview,
		bgColor: "white",
		aspectRatio: 1
	}); 
} 

$('body').on('change', '#photoimg', function() { 
	$("#imageform").ajaxForm({
		success: showResponse
	}).submit();
});

var imageData = {};
$("#image-upload").html(imageTemplate(imageData));

  function checkCoords()
  {
  	 if (parseInt(jQuery('#w').val())>0) return true;
  	 return false;
  };
  
  function showPreview(coords)
  {
    if (parseInt(coords.w) > 0)
    {
      var rx = 300 / coords.w;
      var ry = 300 / coords.h;

      $("#preview").css({
        width: Math.round(rx * $("#jcrop-image").width()) + 'px',
        height: Math.round(ry * $("#jcrop-image").height()) + 'px',
        marginLeft: '-' + Math.round(rx * coords.x) + 'px',
        marginTop: '-' + Math.round(ry * coords.y) + 'px'
      });
      
       jQuery('#x').val(coords.x);
	   jQuery('#y').val(coords.y);
	   jQuery('#w').val(coords.w);
	   jQuery('#h').val(coords.h);
    }
  }
  
  $("#crop").click(function(e) {
  	if (checkCoords()) {
  		$.ajax({
  			url: "/cropimage",
  			dataType: "json",
  			type: "POST",
  			data: {'src': $("#crop-src").val(), 'x': $("#x").val(), 'y': $("#y").val(), 'w': $("#w").val(), 'h': $("#h").val()},
  			success: function(data) {
  			}
  		});
  	}
  });
	
	
});

