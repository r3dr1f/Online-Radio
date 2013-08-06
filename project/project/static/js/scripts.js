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
	'<%- song.name %>'
);

var templateData = {
	name: "Karol kalal drevo"
};

$('#playlist').after(template(templateData));

});
