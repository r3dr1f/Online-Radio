$(document).ready(function() {

function registracia_objavenie_mena_interpreta(){
	$(".trigger").click(function() {
		$('.default_hide').slideToggle("fast");
	});
}

registracia_objavenie_mena_interpreta();

// templateovacia cast

_.templateSettings.variable = "song";
var template = _.template('' + 
	'<div class="song-info">' + 
	'<span class="name">' + 
		'<%- song.interpret %> - <%- song.name %>' + 
	'</span>' + 
	'<span id="song-id"><%- song.id %></span><br />' +
	'<% if (song.rating) { %>' +
		'<span>Vaše hodnotenie: <%- song.rating.rating %></span>' +  
	'<% } else { %>' +
		'<div id="rate">' + 
			'<a href="#" id="rate0">0</a>' + 
			'<a href="#" id="rate1">1</a>' + 
			'<a href="#" id="rate2">2</a>' + 
			'<a href="#" id="rate3">3</a>' + 
			'<a href="#" id="rate4">4</a>' + 
		'</div>' +
	'<% } %>' +  
	'</div>'
);

$("body").on("click", "#playlist a, .jp-title a", function(event){
  event.preventDefault();
  var song_id = $(this).attr("href").split("/");
  song_id = song_id.slice(-1)[0];
  $.ajax({
  	url: "/getsong",
  	type: "post",
  	dataType: "json",
  	data: {id: song_id},
  	success: function(data){
  		if (data.rating != "undefined") {
  			var templateData = {
				name: data.song.name,
				interpret: data.song.interpret.name,
				id: data.song.id,
				rating: data.rating
			};
  		} else {
  			var templateData = {
				name: data.song.name,
				interpret: data.song.interpret.name,
				id: data.song.id
			};
		}
  		$('.song-info').html(template(templateData));
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
			rating: data.rating
		};
  		$('.song-info').html(template(templateData));
  	}
  });
  return false;
});

});
