<%inherit file="default.mako" />
<%block name="title">Úvodná stránka</%block>
<%block name="page_content">
<script type="text/javascript">
$(document).ready(function() {

function setPlaylist(data) {
	table = document.getElementById("playlist");
	table.innerHTML = "";
	for (i = 0; i < data.length; i++) {
		tr = document.createElement("tr");
		td = document.createElement("td");
		interpret = '<a href="interpret/'+data[i].interpret.id + '" class="info-interpret">' + data[i].interpret.name + '</a>';
		song = '<a href="song/'+data[i].song.id + '" class="info-song">' + data[i].song.name + '</a>';
		td.innerHTML = interpret + " - " + song;		
		tr.appendChild(td);
		table.appendChild(tr);
	}	
}

var old_data = "";
var first_time = true;

function callAjax() {
	$.ajax({
		url: "/getsource",
		type: "GET",
		dataType: "json",
		contentType: "json",
		success: function(data) {
			if(JSON.stringify(old_data) != JSON.stringify(data)){
			    old_data = data;
			    if(!first_time){
			    	//$(".jp-title").slideToggle("slow");
			       	//$(".jp-title").delay(2500).slideToggle("slow");
			       	window.setTimeout(function () {
			         	$(".jp-title > a").html('<div class="current-song-image"></div>' + data.song.interpret.name+' - '+data.song.name);
			         	$('.jp-title > a').attr('href',"song/"+data.song.id);
			         	$("#show-playlist").remove();
			         	$(".jp-title").append('<div id="show-playlist"><a href="#">playlist</a></div>');
			        }, 2000);
			        setPlaylist(data.playlist);
			    } else {
		           	first_time = false;
		           	$('.jp-title > a').html('<div class="current-song-image"></div>' + data.song.interpret.name+' - '+data.song.name);
		           	$('.jp-title > a').attr('href',"song/"+data.song.id);
		           	$("#show-playlist").remove();
		           	$(".jp-title").append('<div id="show-playlist"><a href="#">playlist</a></div>');
					setPlaylist(data.playlist);
		        }
        	}	
		}
	});
}	
var interval = window.setInterval(function() {callAjax()}, 5000);

callAjax();

});
</script>
<h2>Toto je úvodná stránka</h2>
 <table id="playlist"></table>
 <div class="song-info"></div>
</%block>
