$(document).ready(function() {

function registracia_objavenie_mena_interpreta(){
	$(".trigger").click(function() {
		$('.default_hide').slideToggle("fast");
	});
}

registracia_objavenie_mena_interpreta();

// templateovacia cast

_.templateSettings.variable = "data";
var songTemplate = _.template('' + 
	'<div class="song-info">' + 
	'<span class="name">' + 
		'<a href="interpret/<%- data.interpret.id %>" class="info-interpret"><%- data.interpret.name %></a> - <%- data.name %>' + 
	'</span>' + 
	'<span id="song-id"><%- data.id %></span><br />' +  
	'<% if (!data.user) { %>' +
	    '<span>Hodnotenie: <%- data.rating %> </span>' +
	'<% } else { if (data.rating) { %>' +
		'<span>Vaše hodnotenie: <%- data.rating.rating %></span>' +
	'<% } else { %>' +
		'<div id="rate">' + 
			'<a href="#" id="rate0">0</a>' + 
			'<a href="#" id="rate1">1</a>' + 
			'<a href="#" id="rate2">2</a>' + 
			'<a href="#" id="rate3">3</a>' + 
			'<a href="#" id="rate4">4</a>' + 
		'</div>' +
	'<% } %>' +
	'<% if (!data.request) {%>' +
		'<a href="request/<%- data.id %>" class="request-to-play">request to play</a>' +
	'<% } else {%>' +
	'<p class="already-requested">Už ste si požiadali o prehratie</p>' +
	'<% }} %>' +
	
	'<% if (data.user) { %>' +
		'<a href="/comment/<%- data.id %>" class="add-comment">Pridať komentár</a><br />' +
		'<form method="POST" action="" id="comment-form">' +
			'<input type="text" id="comment-input" />' +
		'</form>' + 
	'<% } %>' + 
	'<div id="song-comments">' +
	'</div>' + 
	'</div>'
);

var interpretTemplate = _.template('' + 
	'<div class="interpret-info">' + 
	'<span class="name">' + 
		'<%- data.interpret.name %>' + 
	'</span>' +  
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
  	data: {id: $("#song-id").text(), rating: rating},
  	success: function(data){
  		var templateData = {
			name: data.song.name,
			interpret: data.song.interpret.name,
			id: data.song.id,
			rating: data.rating.rating
		};
  		$('.song-info').html(songTemplate(templateData));
  	}
  });
  return false;
});

$("#search-it").click(function(event){
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
	  		$('#rate').after('<p class="already-requested">Váša požiadavka bola zaznamenaná</p>');
  		}
  	}
  });
});

$("body").on("click", ".add-comment", function(event){
	event.preventDefault();
	
	return false;
});

$("body").on("click", ".add-comment", function(event){
	event.preventDefault();
	var song_id = $(this).attr("href").split("/");
  	song_id = song_id.slice(-1)[0];
	$.ajax({
  	url: "/comment",
  	type: "post",
  	dataType: "json",
  	data: {id: song_id},
  	success: function(data){

  	}
  });
});


});
