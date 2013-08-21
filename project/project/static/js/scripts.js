$(document).ready(function() {

// templateovacia cast

_.templateSettings.variable = "data";

var songTemplate = _.template('' + 
	'<div class="song-info">' + 
	'<span class="name">' + 
		'<a href="interpret/<%- data.interpret.id %>" class="info-interpret"><%- data.interpret.name %></a> - <%- data.name %>' + 
	'</span><br />' +
	'<fb:like href="http://localhost:6543/song/<%- data.id %>" width="450" show_faces="true" send="false"></fb:like>' + 
	'<input type="hidden" id="song-id" value="<%- data.id %>" />' +  
	'<% if (!data.user) { %>' +
	    '<span>Hodnotenie: <%- data.rating %> </span><br />' +
	'<% } else { if (data.rating) { %>' +
		'<span>Vaše hodnotenie: <%- data.rating.rating %></span><br />' +
	'<% } else { %>' +
		'<div id="rate">' + 
			'<a href="#" id="rate0">0</a>' + 
			'<a href="#" id="rate1">1</a>' + 
			'<a href="#" id="rate2">2</a>' + 
			'<a href="#" id="rate3">3</a>' + 
			'<a href="#" id="rate4">4</a>' + 
		'</div>' +
	'<% } %>' +
	'<div class="song-rating"></div>' + 
	'<% if (!data.request) {%>' +
		'<a href="request/<%- data.id %>" class="request-to-play">request to play</a><br />' +
	'<% } else {%>' +
	'<p class="already-requested">Už ste si požiadali o prehratie</p>' +
	'<% }} %>' +
	
	'<% if (data.user) { %>' +
		'<br /><a href="/comment/<%- data.id %>" class="add-comment">Pridať komentár</a><br />' +
		'<textarea id="comment-input">' +
		'</textarea>' +
	'<% } %>' + 
	'<div id="song-comments">' +
	'</div>' + 
	'</div>'
);

var commentsTemplate = _.template('' +
	'<% for(var commenti in data.comments) { %>' +
		'<div class="comment"><div class="comment-text"><%- data.comments[commenti].text %></div><div class="comment-time"><%- data.comments[commenti].add_time %></div></div>' +
	'<% } %>'
);

var interpretTemplate = _.template('' + 
	'<div class="interpret-info">' + 
	'<span class="name">' + 
		'<%- data.interpret.name %>' + 
	'</span><br />'+  
	'<div id="interpret-songs">' +
	'<span>Songs:</span><br />' +
	'<% for(var songi in data.songs) { %>' +
		'<a href="/song/<%- data.songs[songi].id %>" class="info-song"><%- data.songs[songi].name %></a><br />' +
	'<% } %>' +
	'</div>' +
	'</div>'
);

var searchTemplate = _.template('' + 
	'<div class="search-results">' +
		'<% if (data.songs.length > 0) { %>' + 
	    '<p>Najdene songy: </p>' +
	    '<% for(var songi in data.songs) {%>' +
		'<a href="song/<%- data.songs[songi].id %>" class="info-song"><%- data.songs[songi].name %></a><br />' +
		'<% } %>' +
		'<% } %>' +
		'<% if (data.interprets.length > 0) { %>' +
		'<p>Najdeni interpreti: </p>' + 
		'<% for(var interpreti in data.interprets) {%>' +
		'<a href="interpret/<%- data.interprets[interpreti].id %>" class="info-interpret"><%- data.interprets[interpreti].name %></a><br />' +
		'<% } %>' +
		'<% } %>' +
		'<% if ((data.songs.length == 0) && (data.interprets.length == 0)) { %>' +
		'<p>Vami vyhladavany vyraz sa nenasiel</p>' +  
		'<% }%>' +
	'</div>'
);

var loginTemplate = _.template('' +
		'<% if (!data.user && !data.register) { %>' +
                '<div id="log in">' +
                    '<form class="login-form" action="#" method="POST">' +
                        '<div class="input-group">' +
                            '<label for="email-login">E-mail</label>' +
                            '<input type="email" name="email" id="email-login" required/>' +
                        '</div>' +
                        '<div class="input-group">' +
                            '<label for="password-login">Heslo</label>' +
                            '<input type="password" name="password" id="password-login" required/>' +    
                        '</div>' +
                        '<button type="submit" id="login" class="submit-form">Prihlásiť sa</button>' +
                        '<a class="register-button" id="fb-login" href="#">Prihlásiť sa pomocou facebooku</a>' +
                        '<a class="register-button" id="register" href="#">Zaregistrovať sa</a>' +
                        '<div class="recovery-password">' +
                        '<a id="beg-for-recovery" href="#" >Zabudol som heslo</a>' +
                        '</div>' +
                    '</form>' +
                '</div>' +
            '<% } if (data.user) { %>' +
                    '<button type="submit" class="signout-button">Odhlásiť <%- data.user.email %></button>' +
            '<% } if (data.register) { %>' +
            	'<form method="POST" id="registracia">' +
				    '<div class="input-group">' +
				        '<label for="email">E-mail</label>' +
				        '<input type="email" name="email" id="email" required/>' +
				    '</div>' +
				    '<div class="input-group">' +
				        '<label for="password">Heslo</label>' +
				        '<input type="password" name="password" id="password" required/>' +
				    '</div>' +
				    '<div class="input-group">' +
				        '<label for="password_repeat">Heslo znovu</label>' +
				        '<input type="password" name="password_repeat" id="password_repeat" required/>' +
				    '</div>' +
				    '<div class="input-group trigger">' +
				        '<label for="role">Sa cítiš, že si interpret?</label>' +
				        '<input type="checkbox" name="role" id="role"/>' +
				    '</div>' +
				    '<div class="input-group default_hide">' +
				        '<label for="interpret_name">Ako ťa ľudia oslovujú?</label>' +
				        '<input type="text" name="interpret_name" id="interpret_name"/>' +
				    '</div>' +
				    '<button type="submit" id="register-submit" class="submit-form">Zaregistrovať sa</button><br />' +
				'</form>' +
				'<% } else if (data.register_success) { %>'+
					'<h4>Boli ste zaregistrovaný. Ejchuchu. </h4>'+
				'<% } %>'
);

$("body").on("click", ".signout-button", function(event){
	event.preventDefault();
	$.ajax({
  	url: "/logout",
  	type: "post",
  	dataType: "json",
  	success: function(data){
  		console.log(data);
  		var loginTemplateData = {
					user: data.user
				};
  		$('.login').html(loginTemplate(loginTemplateData));
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
  		console.log(data);
  		var loginTemplateData = {
					user: data.user
				};
  		$('.login').html(loginTemplate(loginTemplateData));
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
  		$('.login').html(loginTemplate(loginTemplateData));
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
  		$('.login').html(loginTemplate(loginTemplateData));
  	}
  });
	return false;
});

$('body').on("click", ".trigger", function(event){
	$('.default_hide').slideToggle("fast");
});



$("body").on("click", "a.info-interpret", function(event){
  event.preventDefault();
  var interpret_id = $(this).attr("href").split("/");
  interpret_id = interpret_id.slice(-1)[0];
  $.ajax({
  	url: "/getinterpret",
  	type: "post",
  	dataType: "json",
  	data: {id: interpret_id},
  	success: function(data){
  		var templateData = {
					interpret: data.interpret,
					songs: data.songs
				};
  		$('.song-info').html(interpretTemplate(templateData));
  	}
  });
  
  return false;
});

$("body").on("click", "a.info-song, .jp-title a", function(event){
  event.preventDefault();
  var song_id = $(this).attr("href").split("/");
  song_id = song_id.slice(-1)[0];
  $.ajax({
  	url: "/getsong",
  	type: "post",
  	dataType: "json",
  	data: {id: song_id},
  	success: function(data){
  		if (data.user != undefined) {
	  		if (data.rating != undefined) {
	  			var templateData = {
					name: data.song.name,
					interpret: data.song.interpret,
					id: data.song.id,
					rating: data.rating,
					user: data.user,
					request: data.request
				};
			}	else {
				var templateData = {
					name: data.song.name,
					interpret: data.song.interpret,
					id: data.song.id,
					user: data.user,
					request: data.request
				};
			}	
  		} else {
  			var templateData = {
				name: data.song.name,
				interpret: data.song.interpret,
				id: data.song.id,
				rating: data.song.rating_max
			};
		}
  		$('.song-info').html(songTemplate(templateData));
  	}
  });
  
  return false;
});

$("body").on("click", "#rate0, #rate1, #rate2, #rate3, #rate4", function(event){
  event.preventDefault();
  var rating;
  switch ($(this).attr("id")) {
  	case "rate0":
  		rating = 0;
  		break;
  	case "rate1":
  		rating = 1;
  		break;
  	case "rate2":
  		rating = 2;
  		break;
  	case "rate3":
  		rating = 3;
  		break;
  	case "rate4":
  		rating = 4;
  		break;
  }
  $.ajax({
  	url: "/rate",
  	type: "post",
  	dataType: "json",
  	data: {id: $("#song-id").val(), rating: rating},
  	success: function(data){
  		var templateData = {
			name: data.song.name,
			interpret: data.song.interpret,
			id: data.song.id,
			rating: data.rating,
			user: data.user
		};
		var commentsTemplateData = {
			comments: data.comments
		};
  		$('.song-info').html(songTemplate(templateData));
  		$("#song-comments").html(commentsTemplate(commentsTemplateData));
  	}
  });
  return false;
});

$("#search").keypress(function(event){
	if(event.which == 13) {
        if ($(this).val() != "") {
			$.ajax({
			  	url: "/search",
			  	type: "post",
			  	dataType: "json",
			  	data: {search: $("#search").val()},
			  	success: function(data){
			  		var templateData = {
						songs: data.songs,
						interprets: data.interprets
					};
	  				$('#search-info').html(searchTemplate(templateData));
	  			}
  			});
  		}
  	}
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

$("body").on("click", ".request-to-play", function(event){
	event.preventDefault();
	var song_id = $(this).attr("href").split("/");
  	song_id = song_id.slice(-1)[0];
	$.ajax({
  	url: "/request",
  	type: "post",
  	dataType: "json",
  	data: {id: song_id},
  	success: function(data){
  		var templateData = {
			request: data.request
		};
		if(data.request){
			$('.request-to-play').remove();
	  		$('.song-rating').html('<p class="already-requested">Vaša požiadavka bola zaznamenaná</p>');
  		}
  	}
  });
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
	        $.ajax({
			  	url: "/comment",
		  		type: "post",
		  		dataType: "json",
		  		data: {id: $("#song-id").val(), comment: $("#comment-input").val()},
		  		success: function(data){
		  			$("#comment-input").val("");
		  			$("#comment-input").hide();
		  			var templateData = {
		  				comments: data.comments
		  			};
		  			$("#song-comments").html(commentsTemplate(templateData));
	  			}
  			});	
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
											var templateData = {
												user : data.user
											}
											$('.login').html(loginTemplate(templateData));								  		
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
$('.login').html(loginTemplate(loginTemplateData));


$("#login-button > a").click(function(e) {
	e.preventDefault();
	$("#login-content").show();
	return false;
});

$("#login-button > a").blur(function() {
	$("#login-content").hide();
});

});
