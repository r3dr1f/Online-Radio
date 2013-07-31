$(document).ready(function() {

var old_data = "";

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
		    	$(".jp-title ul li").slideToggle("slow");
		    	$(".jp-title ul li").text("");
    			$(".jp-title ul li").delay(2000).slideToggle("slow");
    			window.setTimeout(function () {
    				$(".jp-title ul li").text(data);
				}, 2000);		
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
