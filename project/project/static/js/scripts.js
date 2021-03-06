function getCommentImages(comments) {
	for (var i = 0; i < comments.length; i++) {
		if (comments[i].user.uuid != 0) {
			comments[i].user.img_src = "http://graph.facebook.com/" + comments[i].user.uuid + "/picture?type=square";
		} else {
			if (comments[i].user.image[0] != null) {
				comments[i].user.img_src = "/static/uploaded/" + comments[i].user.id + "/" + comments[i].user.image[0].name;
			} else {
				comments[i].user.img_src = "/static/user-default.jpg";
			}
		}
	}
}

// templateovacia cast

_.templateSettings.variable = "data";

var songTemplate = _.template('' + 
	'<div class="song-info">' + 
	'<span class="name">' + 
		'<a href="interpret/<%- data.interpret.id %>" class="info-interpret"><%- data.interpret.name %></a> - <%- data.name %>' + 
	'</span><br />' +
	'<fb:like href="http://localhost:6543/song/<%- data.id %>" width="450" show_faces="true" send="false"></fb:like>' + 
	'<input type="hidden" id="song-id" value="<%- data.id %>" />' +  
	"<% if (data.user == null || !data.user) { %>" +
	    '<span>Priemerné hodnotenie: <br /> <%- data.rating %>% <span class="stars"><span style="width: <%- Math.max(0, (Math.min(5, parseFloat(data.rating/20.0))))*16 %>px"></span></span> ' +
	'<% } else { if (data.rating != null || data.rating) { %>' +
	   '<span>Priemerné hodnotenie: <br /> <%- data.rating_max %>% <span class="stars"><span style="width: <%- Math.max(0, (Math.min(5, parseFloat(data.rating_max/20.0))))*16 %>px"></span></span> ' +		
		'<span>Tvoje hodnotenie: <span class="stars"> <span style="width: <%- Math.max(0, (Math.min(5, parseFloat(data.rating.rating + 1))))*16 %>px"></span></span> </span><br />' +
	'<% } else { %>' +
		'<br />' +
		'<span>Priemerné hodnotenie: <br /> <%- data.rating_max %>% <span class="stars"><span style="width: <%- Math.max(0, (Math.min(5, parseFloat(data.rating_max/20.0))))*16 %>px"></span></span> ' +		
		'<br />' +		
		'<span>Tvoje hodnotenie: </span> <br />' +		
		'<div id="rate" class="star-rating">' + 
			'<a href="#" id="rate0" class="one-star">0</a>' + 
			'<a href="#" id="rate1" class="two-stars">1</a>' + 
			'<a href="#" id="rate2" class="three-stars">2</a>' + 
			'<a href="#" id="rate3" class="four-stars">3</a>' + 
			'<a href="#" id="rate4" class="five-stars">4</a>' + 
		'</div>' +
	'<% } %>' +
	'<div class="song-rating"></div>' + 
	'<% if (data.request == null || !data.request) {%>' +
		'<a href="request/<%- data.id %>" class="request-to-play">request to play</a><br />' +
	'<% } else {%>' +
	'<p class="already-requested">Už ste si požiadali o prehratie</p>' +
	'<% }} %>' +

	'<% if (data.user != null || data.user) { %>' +
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
		'<div class="comment"><div class="comment-image"><img src="<%- data.comments[commenti].user.img_src %>" /></div><div class="comment-user"><%- data.comments[commenti].user.fullname %></div><div class="comment-text"><%- data.comments[commenti].text %></div><div class="comment-time"><%- data.comments[commenti].add_time %></div></div>' +
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
	'<% if (data.user != null) { %>' +
        '<button type="submit" class="signout-button">Odhlásiť <%- data.user.email %></button>' +
	'<% } else if ((!data.user || data.user == null) && !data.register) { %>' +
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
                '<a class="register-button" id="register" href="#">Zaregistrovať sa</a>' +
                '<a class="register-button" id="fb-login" href="#">&nbsp;</a>' +
                '<div class="recovery-password">' +
                '<a id="beg-for-recovery" href="#" >Zabudol som heslo</a>' +
                '</div>' +
            '</form>' +
    '<% } else if (data.register) { %>' +
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

var imageTemplate = _.template('' +
	'<form id="imageform" method="post" enctype="multipart/form-data" action="/image">' +
		'Upload image <input type="file" name="photoimg" id="photoimg" />' +
	'</form>' +
	'<div id="image">' + 
		'<img src="" alt="skuska" id="jcrop-image"/>' +
	'</div>' +
	'<div id="preview-container">'+
		'<img src="" id="preview" alt="" />' +
	'</div>' +

  	'<input type="hidden" id="crop-src" name="crop-src" value="" />' +
	'<input type="hidden" id="x" name="x" value="0" />' +
	'<input type="hidden" id="y" name="y" value="0" />' +
	'<input type="hidden" id="w" name="w" value="0" />' +
	'<input type="hidden" id="h" name="h" value="0" />' +
	'<input type="submit" value="Orezať" id="crop" />'
);

$(document).ready(function() {



  
  $("body").on("click", "#show-playlist a", function(event) {
  	event.preventDefault();
  	if (!$(".playlist").hasClass("expanded")) {
	  	$(".playlist").animate({width: "20em"}, 1000, "easeInOutQuad", function() {
	  		$(this).addClass("expanded");
	  	});
	  	$("#main").animate({marginLeft: "20em"}, 1000, "easeInOutQuad");
  	} else {
  		$(".playlist").animate({width: 0}, 1000, "easeInOutQuad", function() {
	  		$(this).removeClass("expanded");
	  	});
	  	$("#main").animate({marginLeft: 0}, 1000, "easeInOutQuad");
  	}
  	return false;
  });
  
  $(window).resize(function() {
  	$(".playlist").height($(window).height()-$(".jp-audio").outerHeight(true));
  });
  
  $(".playlist").height($(window).height()-$(".jp-audio").outerHeight(true));
});