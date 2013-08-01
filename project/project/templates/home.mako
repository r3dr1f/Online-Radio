<%inherit file="default.mako" />
<%block name="title">Úvodná stránka</%block>
<%block name="page_content">
<script type="text/javascript">
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

});
</script>
<h2>Toto je úvodná stránka</h2>

<div id="jquery_jplayer_1" class="jp-jplayer"></div>
  <div id="jp_container_1" class="jp-audio">
    <div class="jp-type-single">
      <div class="jp-gui jp-interface">
        <ul class="jp-controls">
          <li><a href="javascript:;" class="jp-play" tabindex="1">play</a></li>
          <li><a href="javascript:;" class="jp-pause" tabindex="1">stop</a></li>
          <li><a href="javascript:;" class="jp-mute" tabindex="1" title="mute">mute</a></li>
          <li><a href="javascript:;" class="jp-unmute" tabindex="1" title="unmute">unmute</a></li>
          <li><a href="javascript:;" class="jp-volume-max" tabindex="1" title="max volume">max volume</a></li>
        </ul>
        <div class="jp-volume-bar">
          <div class="jp-volume-bar-value"></div>
        </div>
      </div>
      <div class="jp-title">
        <ul>
          <li>&nbsp;</li>
        </ul>
      </div>
      <div class="jp-no-solution">
        <span>Update Required</span>
        To play the media you will need to either update your browser to a recent version or update your <a href="http://get.adobe.com/flashplayer/" target="_blank">Flash plugin</a>.
      </div>
    </div>
  </div>
</%block>
