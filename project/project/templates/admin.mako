<%inherit file="default.mako" />
<%block name="title">Admin</%block>
<%block name="page_content">
<h2>Toto je administratorske rozhranie</h2>
	% if request.isOpenedStream is None:
		<form action="${request.route_path('admin')}" method="POST">
			<button type="submit" class="submit-form">Zapnut stream</button>
		</form>
	% else:	
    		<div> ${stdout} </div>
	% endif
</%block>
