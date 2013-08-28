_.templateSettings.variable = "data";

var songTemplate = _.template('' + 
	'<div class="song-info">' + 
	'<span class="name">' + 
		'<a href="interpret/<%- data.interpret.id %>" class="info-interpret"><%- data.interpret.name %></a> - <%- data.name %>' + 
	'</span><br />' +
	'<fb:like href="http://localhost:6543/song/<%- data.id %>" width="450" show_faces="true" send="false"></fb:like>' + 
	'<input type="hidden" id="song-id" value="<%- data.id %>" />' +  
	'<% if (data.user == null || !data.user) { %>' +
	    '<span>Hodnotenie: <%- data.rating %> </span><br />' +
	'<% } else { if (data.rating != null || data.rating) { %>' +
		'<span>Vaše hodnotenie: <%- data.rating.rating %></span><br />' +
	'<% } else { %>' +
		'<div id="rate">' + 
			'<a href="#" id="rate0">0</a>' + 
			'<a href="#" id="rate1">1</a>' + 
			'<a href="#" id="rate2">2</a>' + 
			'<a href="#" id="rate3">3</a>' + 
			'<a href="#" id="rate4">4</a>' + 
		'</div>' +
	'<% } %>' +
	'<div class="song-rating"></div>' + 
	'<% if (data.request == null || !data.request) {%>' +
		'<a href="request/<%- data.id %>" class="request-to-play">request to play</a><br />' +
	'<% } else {%>' +
	'<p class="already-requested">Už ste si požiadali o prehratie</p>' +
	'<% }} %>' +

	'<% if (data.user != null || data.user) { %>' +
		'<br /><a href="/comment/<%- data.id %>" class="add-comment">Pridať komentár</a><br />' +
		'<textarea id="comment-input">' +
		'</textarea>' +
	'<% } %>' + 
	'<div id="song-comments">' +
	'</div>' + 
	'</div>'
);

var commentsTemplate = _.template('' +
	'<% for(var commenti in data.comments) { %>' +
		'<div class="comment"><div class="comment-text"><%- data.comments[commenti].text %></div><div class="comment-time"><%- data.comments[commenti].add_time %></div></div>' +
	'<% } %>'
);

var interpretTemplate = _.template('' + 
	'<div class="interpret-info">' + 
	'<span class="name">' + 
		'<%- data.interpret.name %>' + 
	'</span><br />'+  
	'<div id="interpret-songs">' +
	'<span>Songs:</span><br />' +
	'<% for(var songi in data.songs) { %>' +
		'<a href="/song/<%- data.songs[songi].id %>" class="info-song"><%- data.songs[songi].name %></a><br />' +
	'<% } %>' +
	'</div>' +
	'</div>'
);

var searchTemplate = _.template('' + 
	'<div class="search-results">' +
		'<% if (data.songs.length > 0) { %>' + 
	    '<p>Najdene songy: </p>' +
	    '<% for(var songi in data.songs) {%>' +
		'<a href="song/<%- data.songs[songi].id %>" class="info-song"><%- data.songs[songi].name %></a><br />' +
		'<% } %>' +
		'<% } %>' +
		'<% if (data.interprets.length > 0) { %>' +
		'<p>Najdeni interpreti: </p>' + 
		'<% for(var interpreti in data.interprets) {%>' +
		'<a href="interpret/<%- data.interprets[interpreti].id %>" class="info-interpret"><%- data.interprets[interpreti].name %></a><br />' +
		'<% } %>' +
		'<% } %>' +
		'<% if ((data.songs.length == 0) && (data.interprets.length == 0)) { %>' +
		'<p>Vami vyhladavany vyraz sa nenasiel</p>' +  
		'<% }%>' +
	'</div>'
);

var loginTemplate = _.template('' +
	'<% if (!data.user && !data.register) { %>' +
        '<div id="log-in">' +
            '<form class="login-form" action="#" method="POST">' +
                '<div class="input-group">' +
                    '<label for="email-login">E-mail</label>' +
                    '<input type="email" name="email" id="email-login" required/>' +
                '</div>' +
                '<div class="input-group">' +
                    '<label for="password-login">Heslo</label>' +
                    '<input type="password" name="password" id="password-login" required/>' +    
                '</div>' +
                '<button type="submit" id="login" class="submit-form">Prihlásiť sa</button>' +
                '<a class="register-button" id="register" href="#">Zaregistrovať sa</a>' +
                '<a class="register-button" id="fb-login" href="#">&nbsp;</a>' +
                '<div class="recovery-password">' +
                '<a id="beg-for-recovery" href="#" >Zabudol som heslo</a>' +
                '</div>' +
            '</form>' +
        '</div>' +
    '<% } if (data.user) { %>' +
        '<button type="submit" class="signout-button">Odhlásiť <%- data.user.email %></button>' +
    '<% } if (data.register) { %>' +
      	'<form method="POST" id="registracia">' +
		    '<div class="input-group">' +
		        '<label for="email">E-mail</label>' +
		        '<input type="email" name="email" id="email" required/>' +
		    '</div>' +
		    '<div class="input-group">' +
		        '<label for="password">Heslo</label>' +
		        '<input type="password" name="password" id="password" required/>' +
		    '</div>' +
		    '<div class="input-group">' +
		        '<label for="password_repeat">Heslo znovu</label>' +
		        '<input type="password" name="password_repeat" id="password_repeat" required/>' +
		    '</div>' +
		    '<div class="input-group trigger">' +
		        '<label for="role">Sa cítiš, že si interpret?</label>' +
		        '<input type="checkbox" name="role" id="role"/>' +
		    '</div>' +
		    '<div class="input-group default_hide">' +
		        '<label for="interpret_name">Ako ťa ľudia oslovujú?</label>' +
		        '<input type="text" name="interpret_name" id="interpret_name"/>' +
		    '</div>' +
		    '<button type="submit" id="register-submit" class="submit-form">Zaregistrovať sa</button><br />' +
		'</form>' +
		'<% } else if (data.register_success) { %>'+
			'<h4>Boli ste zaregistrovaný. Ejchuchu. </h4>'+
		'<% } %>'
);

