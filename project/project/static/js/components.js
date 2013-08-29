function Song_info(id) {
	this.data = {};
	this.render = function() {
		if (this.data.user != undefined) {
	  		if (this.data.rating != undefined) {
	  			var templateData = {
					name: this.data.song.name,
					interpret: this.data.song.interpret,
					id: this.data.song.id,
					rating: this.data.rating,
					rating_max: this.data.song.rating_max,
					user: this.data.user,
					request: this.data.request
				};
			}	else {
				var templateData = {
					name: this.data.song.name,
					interpret: this.data.song.interpret,
					id: this.data.song.id,
					rating_max: this.data.song.rating_max,	
					user: this.data.user,
					request: this.data.request
				};
			}	
  		} else {
  			var templateData = {
				name: this.data.song.name,
				interpret: this.data.song.interpret,
				id: this.data.song.id,
				rating: this.data.song.rating_max
			};
		}
		$(this.element).html(songTemplate(templateData));
		getCommentImages(this.data.comments);
  		if (this.data.comments != undefined) {
			var commentsTemplateData = {
				comments: this.data.comments
			};
	  		$("#song-comments").html(commentsTemplate(commentsTemplateData));
  		}
	}
	function fetch_data(id, done_callback){
		$.ajax({
	  	url: "/getsong",
	  	type: "post",
	  	dataType: "json",
	  	data: {id: id},
	  	success: done_callback
	 	});
	}
	this.enter = function(element){
		var me = this;
		this.element = element;
		fetch_data(id, function(data){
			me.data = data;
			me.render();
			me.register_events();
		});
	}
	this.register_events = function(){
		$('a.info-interpret', this.element).click(function(ev){
			ev.preventDefault();
			var interpret_id = $(this).attr("href").split("/");
			interpret_id = interpret_id.slice(-1)[0];
			$('a.info-interpret', this.element).trigger('interpret-info-request', [interpret_id]);
		});
		$("#rate0, #rate1, #rate2, #rate3, #rate4", this.element).click(function(ev){
			ev.preventDefault();
			var rating;
			switch ($(this).attr("id")) {
				case "rate0":
			  		rating = 0;
			  		break;
			  	case "rate1":
			  		rating = 1;
			  		break;
			  	case "rate2":
			  		rating = 2;
			  		break;
			  	case "rate3":
			  		rating = 3;
			  		break;
			  	case "rate4":
			  		rating = 4;
			  		break;
			}
			$('#rate0, #rate1, #rate2, #rate3, #rate4', this.element).trigger('rate-info-request', [id, rating]);
		});
		$(".request-to-play").click(function(ev){
			ev.preventDefault();
			$('.request-to-play').trigger('request-info-request', [id]);
		});
	}
	this.exit = function(){
		$("body").off("click", "#rate0, #rate1, #rate2, #rate3, #rate4");//, a.request-to-play, a.info-interpret");
	}
	this.user_login = function(user_id){
		this.data.user = user_id;
		this.render();
	}
}

function Interpret_info(id){
	this.data = {};
	this.render = function(){
		var templateData = {
			interpret: this.data.interpret,
			songs: this.data.songs
		};
		$(this.element).html(interpretTemplate(templateData));
	}
	this.fetch_data = function(id, done_callback){
		$.ajax({
	  	url: "/getinterpret",
	  	type: "post",
	  	dataType: "json",
	  	data: {id: id},
	  	success: done_callback
	  	});
	}
	this.enter = function(element){
		var me = this;
		this.element = element;
		this.fetch_data(id, function(data){
			me.data = data;
			me.render();
			me.register_events();
		});
	}
	this.register_events = function(){
		$('a.info-song', this.element).click(function(ev){
			ev.preventDefault();
			var song_id = $(this).attr("href").split("/");
			song_id = song_id.slice(-1)[0];
			$(this).trigger('song-info-request', [song_id]);
		});
	}
	this.exit = function(){
		$('a.info-song').off("click");		
	}
	this.user_login = function(user_id){
		this.data.user = user_id;
		this.render();
	}
}

function Search_info(param){
	this.data = {};
	this.render = function(){
		var templateData = {
			songs: this.data.songs,
			interprets: this.data.interprets
		};
		$(this.element).html(searchTemplate(templateData));
	}
	this.fetch_data = function(param, done_callback){
		$.ajax({
	  	url: "/search",
		type: "post",
		dataType: "json",
		data: {search: param},
		success: done_callback
	  	});
	}
	this.enter = function(element){
		var me = this;
		this.element = element;
		this.fetch_data(param, function(data){
			me.data = data;
			me.render();
			me.register_events();
		});
	}
	this.register_events = function(){
		$('a.info-song', this.element).click(function(ev){
			ev.preventDefault();
			var song_id = $(this).attr("href").split("/");
			song_id = song_id.slice(-1)[0];
			$(this).trigger('song-info-request', [song_id]);
		});
		$('a.info-interpret', this.element).click(function(ev){
			ev.preventDefault();
			var interpret_id = $(this).attr("href").split("/");
			interpret_id = interpret_id.slice(-1)[0];
			$('a.info-interpret', this.element).trigger('interpret-info-request', [interpret_id]);
		});
	}
	this.exit = function(){
		$('.song-info *').off("click");		
	}
	this.user_login = function(user_id){
		this.data.user = user_id;
		this.render();
	}
}

function Comments_info(id, comment){
	this.data = {};
	this.render = function(){
		getCommentImages(this.data.comments);
		var templateData = {
			comments: this.data.comments
		};
		$(this.element).html(commentsTemplate(templateData));
	}
	this.fetch_data = function(id, comment, done_callback){
		$.ajax({
	  	url: "/comment",
		type: "post",
		dataType: "json",
		data: {id: id, comment: comment},
		success: done_callback
	  	});
	}
	this.enter = function(element){
		var me = this;
		this.element = element;
		this.fetch_data(id, comment, function(data){
			me.data = data;
			me.render();
			me.register_events();
			$("#comment-input").val("");
			$("#comment-input").hide();
		});
	}
	this.register_events = function(){
		$('a.info-song', this.element).click(function(ev){
			ev.preventDefault();
			var song_id = $(this).attr("href").split("/");
			song_id = song_id.slice(-1)[0];
			$(this).trigger('song-info-request', [song_id]);
		});
		$('a.info-interpret', this.element).click(function(ev){
			ev.preventDefault();
			var interpret_id = $(this).attr("href").split("/");
			interpret_id = interpret_id.slice(-1)[0];
			$('a.info-interpret', this.element).trigger('interpret-info-request', [interpret_id]);
		});
	}
	this.exit = function(){
		$('.song-info *').off("click");		
	}
	this.user_login = function(user_id){
		this.data.user = user_id;
		this.render();
	}
}

function Rating_info(id, rating){
	this.data = {};
	this.render = function(){
		var templateData = {
				name: this.data.song.name,
				interpret: this.data.song.interpret,
				id: this.data.song.id,
				rating: this.data.rating,
				rating_max: this.data.song.rating_max,
				user: this.data.user
			};
		var commentsTemplateData = {
				comments: this.data.comments
		};
		$(this.element).html(songTemplate(templateData));
	  	$('#song-comments', this.element).html(commentsTemplate(commentsTemplateData));
	}
	this.fetch_data = function(id, rating, done_callback){
		$.ajax({
	  	url: "/rate",
	  	type: "post",
	  	dataType: "json",
	  	data: {id: id, rating: rating},
	  	success: done_callback
	  	});
	}
	this.enter = function(element){
		var me = this;
		this.element = element;
		this.fetch_data(id, rating, function(data){
			me.data = data;
			me.render();
			me.register_events();
		});
	}
	this.register_events = function(){
		$('a.info-song', this.element).click(function(ev){
			ev.preventDefault();
			var song_id = $(this).attr("href").split("/");
			song_id = song_id.slice(-1)[0];
			$(this).trigger('song-info-request', [song_id]);
		});
		$('a.info-interpret', this.element).click(function(ev){
			ev.preventDefault();
			var interpret_id = $(this).attr("href").split("/");
			interpret_id = interpret_id.slice(-1)[0];
			$('a.info-interpret', this.element).trigger('interpret-info-request', [interpret_id]);
		});
	}
	this.exit = function(){
		$('.song-info *').off("click");		
	}
	this.user_login = function(user_id){
		this.data.user = user_id;
		this.render();
	}
}

function Request_info(id){
	this.data = {};
	this.render = function(){
		if(this.data.request){
				$('.request-to-play').remove();
		  		$('.song-rating', this.element).html('<p class="already-requested">Vaša požiadavka bola zaznamenaná</p>');
  		}
	}
	this.fetch_data = function(id, done_callback){
		$.ajax({
	  	url: "/request",
	  	type: "post",
	  	dataType: "json",
	  	data: {id: id},
	  	success: done_callback
	  	});
	}
	this.enter = function(element){
		var me = this;
		this.element = element;
		this.fetch_data(id, function(data){
			me.data = data;
			me.render();
			me.register_events();
		});
	}
	this.register_events = function(){
		$('a.info-song', this.element).click(function(ev){
			ev.preventDefault();
			var song_id = $(this).attr("href").split("/");
			song_id = song_id.slice(-1)[0];
			$(this).trigger('song-info-request', [song_id]);
		});
		$('a.info-interpret', this.element).click(function(ev){
			ev.preventDefault();
			var interpret_id = $(this).attr("href").split("/");
			interpret_id = interpret_id.slice(-1)[0];
			$('a.info-interpret', this.element).trigger('interpret-info-request', [interpret_id]);
		});
	}
	this.exit = function(){
		$('.song-info *').off("click");		
	}
	this.user_login = function(user_id){
		this.data.user = user_id;
		this.render();
	}
}