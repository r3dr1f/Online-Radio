$(document).ready(function() {

function registracia_objavenie_mena_interpreta(){
	$(".trigger").click(function() {
		$('.default_hide').slideToggle("fast");
	});
}

registracia_objavenie_mena_interpreta();

// templateovacia cast

_.templateSettings.variable = "song";
var template = _.template(
	'<%- song.interpret %> - <%- song.name %>'
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
  		console.log(data);
  		var templateData = {
			name: data.song.name,
			interpret: data.song.interpret.name
		};
  		$('.song-info').html(template(templateData));
  	}
  });
  
  return false;
});

});
