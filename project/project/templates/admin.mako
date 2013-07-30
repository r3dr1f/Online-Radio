<%inherit file="default.mako" />
<%block name="title">Admin</%block>
<%block name="page_content">
<h2>Toto je administratorske rozhranie</h2>
	<form action="${request.route_path('admin')}" method="POST">
		<button type="submit" class="submit-form">Zapnut stream</button>
	</form>
</%block>
