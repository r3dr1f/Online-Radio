$(document).ready(function() {

var old_data = "";
var first_time = true;

function callAjax() {
	$.ajax({
		//url: "http://localhost:1234/requests/status.xml",
		url: "/getsource",
		type: "GET",
		dataType: "html",
		contentType: "html",
		success: function(data) {
			if(old_data != data){
		    	old_data = data;
		    	if(!first_time){
		    		$(".jp-title ul li").slideToggle("slow");
    				$(".jp-title ul li").delay(2500).slideToggle("slow");
    				window.setTimeout(function () {
    					$(".jp-title ul li").text(data);
					}, 2000);	
    			} else {
    				first_time = false;
    				$('.jp-title ul li').text(data);
    			}	
    		}
		}
	});
}	
var interval = window.setInterval(function() {callAjax()}, 5000);

callAjax();

$(".trigger").click(function() {
	$('.default_hide').slideToggle("5000");
});

});
