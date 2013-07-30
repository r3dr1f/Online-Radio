$(document).ready(function() {

function callAjax() {
	$.ajax({
		//url: "http://localhost:1234/requests/status.xml",
		url: "/getsource",
		type: "GET",
		dataType: "html",
		contentType: "html",
		success: function(data) {
    		$(".jp-title ul li").text(data);
		}
	});
}	
var interval = window.setInterval(function() {callAjax()}, 5000);

});
