<%inherit file="default.mako" />
<%block name="page_content">
<img src="${request.static_path('project:static/uploaded/skuska3.gif')}" alt="skuska" id="jcrop-image"/>
<div id="preview-container">
	<img src="${request.static_path('project:static/uploaded/skuska3.gif')}" id="preview" alt="" />
</div>


<form action="${request.route_path('image')}" id="crop-form" method="POST" onsubmit="return checkCoords();">
  <input type="hidden" id="x" name="x" value="0" />
  <input type="hidden" id="y" name="y" value="0" />
  <input type="hidden" id="w" name="w" value="0" />
  <input type="hidden" id="h" name="h" value="0" />
  <input type="submit" value="Orezať" />
</form>


<script type="text/javascript">
  $(document).ready(function() {
  
  function checkCoords()
  {
  	 if (parseInt(jQuery('#w').val())>0) return true;
  	 return false;
  };
  
  function showPreview(coords)
  {
    if (parseInt(coords.w) > 0)
    {
      var rx = 300 / coords.w;
      var ry = 300 / coords.h;

      $("#preview").css({
        width: Math.round(rx * $("#jcrop-image").width()) + 'px',
        height: Math.round(ry * $("#jcrop-image").height()) + 'px',
        marginLeft: '-' + Math.round(rx * coords.x) + 'px',
        marginTop: '-' + Math.round(ry * coords.y) + 'px'
      });
      
       jQuery('#x').val(coords.x);
	   jQuery('#y').val(coords.y);
	   jQuery('#w').val(coords.w);
	   jQuery('#h').val(coords.h);
    }
  }
    
    $('#jcrop-image').Jcrop({
		  onChange: showPreview,
		  onSelect: showPreview,
		  aspectRatio: 1
	 });
  });
</script>
</%block>