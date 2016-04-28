var LinkData = function(link , videoId , name , linkId){
	this.link = link;
	this.videoId = videoId;
	this.name = name;
	this.linkId = linkId;
	this.getHtmlStr = function(){
		//console.log("this.videoId : " + this.videoId);
		var str = '<div class = "link" id ="' + this.videoId + '" ondblclick="Controller.playVideoByLink(\'' +  this.videoId + '\');"> ' + this.name + '</div>';
		return str;
	}
};

/*
Object.defineProperties(LinkData.prototype , {
	,
});
*/
var ModelLibrary = {
	library : {},
	currentLink : null,
	totalLinks : 0,
	initUrl :  null ,
	linkUrl : null ,
	playlistUrl : null , 
	links : {} , 
	playlists : {} ,
	init : function(initUrl , linkUrl , playlistUrl){
		this.initUrl = initUrl;
		this.linkUrl = linkUrl;
		this.playlistUrl = playlistUrl;
		this.library = {};

		//console.log(this.initUrl + '\n' + this.linkUrl + '\n' + this.playlistUrl);

		$.ajax({
		    url: this.initUrl ,
		    type: "POST" , 
		    dataType: "json" ,
		    contentType: 'application/json; charset=utf-8',
		    success: function(resultData) {
		    	ModelLibrary.links = resultData["links"];
		    	

		    	var linklist = [];
		    	for (var link in resultData["links"]) {
				    // skip loop if the property is from prototype
				    if (!resultData["links"].hasOwnProperty(link)) continue;

				    linklist.push(link);
				}

				/*
				var obj = resultData["links"][link];
			    var videoLink = obj["link"];
			    var videoName = obj["name"];
			    var videoid = ModelLibrary.extractVideoId(videoLink);
			    this.library[videoid] = {};
				this.library[videoid] = new LinkData(videoLink , videoid , videoName);
				this.totalLinks ++;
				*/
				
				
				ModelLibrary.playlists = {};
				ModelLibrary.playlists["All Songs"] = {
					"linklist" : linklist , 
					"id" : 0
				};
				console.log(ModelLibrary.playlists["All Songs"]);
				for (var playlist in resultData["playlists"]){
					// skip loop if the property is from prototype
				    if (!resultData["playlists"].hasOwnProperty(playlist)) continue;

				    var obj = resultData["playlists"][playlist];
				    var name = obj["name"];
				    linklist = obj["links"];
				    ModelLibrary.playlists[name] = {
				    	"linklist" : linklist , 
				    	"id" : playlist
				    };
				}

				ModelLibrary.updatePlaylist("All Songs");
				for(var link in ModelLibrary.library){
					ModelLibrary.currentLink = link;
					break;
				}
				Controller.viewlistRender();
		    },
		    error : function(jqXHR, textStatus, errorThrown) {
				console.log("ajax error");
				console.log(jqXHR);
				console.log(textStatus);
				console.log(errorThrown);
		    }
		});
	},
	getCurrentLink : function(){
		return this.currentLink;
	},
	setCurrentLink : function(link){
		this.currentLink = link;
	},
	getTotalLinks : function(){
		return this.totalLinks;
	},
	getLinkData : function(link){
		return this.library[link];
	},
	addLinkData : function(link , data){
		this.library[link] = data;
		this.totalLinks ++;
	},
	deleteLinkData : function(link){
		delete this.library[link];
		this.totalLinks --;
	},
	getLibrary : function(){
		console.log("hello there");
		return this.library;
	},
	checkIfLinkExists : function(link){
		if(this.library[link]){
			return true;
		}
		else{
			return false;
		}
	},
	extractVideoId : function(link){
		var videoid = link.match(/(?:https?:\/{2})?(?:w{3}\.)?youtu(?:be)?\.(?:com|be)(?:\/watch\?v=|\/)([^\s&]+)/);
		if(videoid != null) {
		   return videoid[1];
		} else { 
		    return null;
		}
	},
	getPlaylists : function(){
		var list = [];
		for (var playlist in this.playlists){
			// skip loop if the property is from prototype
			if (!(this.playlists).hasOwnProperty(playlist)) continue;
			list.push(playlist);
		}
		return list;
	},
	updatePlaylist : function(playlist){
		console.log(this.playlists[playlist]["linklist"]);
		var list = this.playlists[playlist]["linklist"];
		var tempLibrary = {};
		var totalLinks = 0;
		
		for (var i = 0; i < list.length ; i++){
			id = list[i];
			//console.log(id);
			var obj = ModelLibrary.links[id];
		    var videoLink = obj["link"];
		    var videoName = obj["name"];
		    var videoid = this.extractVideoId(videoLink);	
			tempLibrary[videoid] = new LinkData(videoLink , videoid , videoName , id);
			totalLinks ++;
		}
		this.library = tempLibrary;
		this.totalLinks = totalLinks;
	},
	serverAddLink : function(LinkName , myLink , playlist){
		console.log(LinkName , myLink)
		var operation = "add";
		var mydata = {
			"operation" : operation , 
			"name" : LinkName , 
			"link" : myLink , 
			"playlist" : playlist
		};
		$.ajax({
		    url: this.linkUrl ,
		    type: "POST" , 
		    dataType: "json" ,
		    contentType: 'application/json; charset=utf-8',
		    data : JSON.stringify(mydata),
		    success: function(resultData) {
		    	// some event 
		    	console.log("Added link");
		    },
		    error : function(jqXHR, textStatus, errorThrown) {
				
		    }
		});
	},
	getPlaylistId : function(playlist){
		return this.playlists[playlist]["id"];
	}
};

var Controller = {
	myLink : null,
	myLinkData : null,
	linkClass : null,
	init : function(initUrl , linkUrl , playlistUrl){
		ViewFrame.init();
		ModelLibrary.init(initUrl , linkUrl , playlistUrl);
		this.linkClass = "link";
	},
	getLibrary : function(){
		return ModelLibrary.getLibrary();
	},
	getCurrentLink : function(){
		return ModelLibrary.getCurrentLink();
	},
	getTotalLinks : function(){
		return ModelLibrary.getTotalLinks();
	},
	onStateChange : function(event){
		if(event.data == YT.PlayerState.ENDED){
			Controller.playNextVideo();
		}
		else if(event.data == YT.PlayerState.PLAYING){
			ViewFrame.setPlayerState("playing");
		}
		else if(event.data == YT.PlayerState.PAUSED){
			ViewFrame.setPlayerState("paused");
		}
		/*else if(event == YT.PlayerState.BUFFERING){
			
		}
		else if(event == YT.PlayerState.CUED){
			
		}*/
	},
	playVideoByLink : function(link){
		var prevlink = ModelLibrary.getCurrentLink();
		ViewList.highlightLink(prevlink , link);
		this.myLinkData = ModelLibrary.getLinkData(link);
		ModelLibrary.setCurrentLink(link);
		ViewFrame.setVideoDetails(this.myLinkData);
		ViewFrame.playVideoById(this.myLinkData.videoId);
	},
	playNextVideo : function(){
		this.myLink = this.getCurrentLink();
		if($("#" + this.myLink).next("." + this.linkClass).length){
			this.myLink = $('#' + this.myLink).next("." + this.linkClass).attr('id');
		}
		else{
			this.myLink = $("." + this.linkClass).first().attr('id');
		}
		this.playVideoByLink(this.myLink);
	},
	playPreviousVideo : function(){
		this.myLink = this.getCurrentLink();
		if($('#' + this.myLink).prev("." + this.linkClass).length){
			this.myLink =  $('#' + this.myLink).prev("." + this.linkClass).attr('id');
		}
		else{
			this.myLink =  $("." + this.linkClass).last().attr('id');
		}
		this.playVideoByLink(this.myLink);
	},
	playPauseVideo : function(){
		ViewFrame.playPauseVideo();
	},
	addLink : function(){
		var link = document.getElementById('link');
		var name = document.getElementById('name');
		var videoId = ModelLibrary.extractVideoId(link.value);
		
		if(link.value && name.value && videoId){
			var linkData = new LinkData(link.value , videoId , name.value );
			ModelLibrary.addLinkData(videoId , linkData);
			ViewList.addLink(linkData);
		}
		var playlist = getCurrentPlaylist();
		playlist = getPlaylistId(playlist);
		ModelLibrary.serverAddLink(name.value , link.value , playlist);
		link.value = null;
		name.value = null;
		return false;
	},
	removeLink : function(){
		
	},
	getPlaylists : function(){
		return ModelLibrary.getPlaylists();
	},
	changeLinkList : function(){
		var playlist = getCurrentPlaylist();
		ModelLibrary.updatePlaylist(playlist);
		var library = ModelLibrary.getLibrary();
		ViewList.renderLinkList(library);
	},
	viewlistRender : function(){
		ViewList.render();
	}
};

var ViewList = {
	render : function(){
		var mylibrary = Controller.getLibrary();
		console.log(mylibrary);
		ViewList.renderLinkList(mylibrary);
		var myPlaylists = Controller.getPlaylists();
		console.log(myPlaylists);
		for (var i = 0; i < myPlaylists.length ; i++){
			name = myPlaylists[i];
			this.addPlaylist(name);
		}
	},
	addLink : function(myLinkData){
		var myLinkList = $('#linklist');
		var str = myLinkData.getHtmlStr();
		myLinkList.append(str);
	},
	addPlaylist : function(playlist){
		var str = '<option class = "playlist" id ="' + playlist + '" ondblclick="Controller.loadPlaylist(\'' +  playlist + '\');"> ' + playlist + '</option>';
		$("#PlaylistSelect").append(str);
	},
	highlightLink : function(prevLink , myLink){
		var prevelem = $("#" + prevLink);
		var newelem = $("#" + myLink);

		prevelem.removeClass("highlight");
		newelem.addClass("highlight");
	},
	renderLinkList : function(mylibrary){
		var myLinkList = document.getElementById('linklist');
		var myLinkData = null;
		var auxstr = '';
		for( var i in mylibrary)
		{
			myLinkData = mylibrary[i];
			var str = myLinkData.getHtmlStr();
			auxstr = auxstr + str;
			//console.log("i : " + i + " str : " + str);
		}
		myLinkList.innerHTML = auxstr;
		//console.log(auxstr);
	},
	getCurrentPlaylist : function(){
		return $('select[name=PlaylistSelect]').val();
	}
};

function onYouTubeIframeAPIReady() {
	ViewFrame.player = new YT.Player('player', {
		height: '450',
		width: '750',
		events: {
		'onReady': ViewFrame.setPlayerReady,
		//'onError' : ViewFrame.onError,
		'onStateChange' : Controller.onStateChange
		//'onPlaybackQualityChange' : ViewFrame.onPlaybackQualityChange,
		//'onPlaybackRateChange' : ViewFrame.onPlaybackRateChange
		}
	});
}

var ViewFrame = {
	player : null,
	ready : false,
	playerState : null,
	init : function(){
		var tag = document.createElement('script');
		tag.src = "https://www.youtube.com/iframe_api";
		var firstScriptTag = document.getElementsByTagName('script')[0];
		firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
	},
	setPlayerReady : function(event){
		this.ready = true;
	},
	playVideoById : function(videoId){
		this.player.loadVideoById( videoId );
		this.playerState = "playing";
	},
	setVideoDetails : function(myLinkData){
		var myLinkName = document.getElementById('linkname');
		myLinkName.innerHTML = myLinkData.name;
	},
	playPauseVideo : function(){

		if(this.playerState == "paused"){
			this.player.playVideo();	
		}
		else if(this.playerState == "playing"){
			this.player.pauseVideo();
		}
		console.log(this.playerState);
	},
	setPlayerState : function(state){
		this.playerState = state;
	},
	getPlayerState : function(state){
		return this.playerState;
	}
};

