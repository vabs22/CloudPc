var LinkData = function(link , videoId , name , duration){
	this.link = link;
	this.videoId = videoId;
	this.name = name;
	this.duration = duration;
	this.getHtmlStr = function(){
		//console.log("this.videoId : " + this.videoId);
		var str = '<div class = "link" id ="' + this.videoId + '" ondblclick="Controller.playVideoByLink(\'' +  this.videoId + '\');"> ' + this.name + '</div>';
		return str
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
	totalLinks : null,
	init : function(){
		this.library['Y2HLFS86v04'] = new LinkData("Y2HLFS86v04" , "Y2HLFS86v04" , "tvf permanent roomates preview" , "11:46");
		this.library['jE1j5Om7g0U'] = new LinkData("jE1j5Om7g0U" , "jE1j5Om7g0U" , "tedx you are awesome" , "10:20");
		this.library['ZszlVVY1LXo'] = new LinkData("ZszlVVY1LXo" , "ZszlVVY1LXo" , "raspberry pi hacks" , "8:40");
		this.library['_aAA9-edO3I'] = new LinkData("_aAA9-edO3I" , "_aAA9-edO3I" , "change" , "11:46");
		this.totalLinks = 4;
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
		return this.library;
	},
	checkIfLinkExists : function(link){
		if(this.library[link]){
			return true;
		}
		else{
			return false;
		}
	}
};

var Controller = {
	myLink : null,
	myLinkData : null,
	linkClass : null,
	init : function(){
		ViewFrame.init();
		ModelLibrary.init();
		ViewList.render();
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
	extractVideoId : function(link){
		var videoid = link.match(/(?:https?:\/{2})?(?:w{3}\.)?youtu(?:be)?\.(?:com|be)(?:\/watch\?v=|\/)([^\s&]+)/);
		if(videoid != null) {
		   return videoid[1];
		} else { 
		    return null;
		}
	},
	addLink : function(){
		var link = document.getElementById('link');
		var name = document.getElementById('name');
		var duration = document.getElementById('duration');
		var videoId = this.extractVideoId(link.value);
		
		if(link.value && name.value && duration.value && videoId){
			var linkData = new LinkData(link.value , videoId , name.value , duration.value);
			ModelLibrary.addLinkData(videoId , linkData);
			ViewList.addLink(linkData);
		}
		link.value = null;
		name.value = null;
		duration.value = null;
		return false;
	},
	removeLink : function(){
		
	}
};

var ViewList = {
	render : function(){

		var myLinkList = document.getElementById('linklist');
		var mylibrary = Controller.getLibrary();
		var myLinkData = null;
		var auxstr = '';
		for( var i in mylibrary)
		{
			myLinkData = mylibrary[i];
			var str = myLinkData.getHtmlStr();
			auxstr = auxstr + str;
		}
		myLinkList.innerHTML = auxstr;
	},
	addLink : function(myLinkData){
		var myLinkList = $('#linklist');
		var str = myLinkData.getHtmlStr();
		myLinkList.append(str);
	},
	highlightLink : function(prevLink , myLink){
		var prevelem = $("#" + prevLink);
		var newelem = $("#" + myLink);

		prevelem.removeClass("highlight");
		newelem.addClass("highlight");
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
		var myLinkDuration = document.getElementById('linkduration');
		myLinkDuration.innerHTML = myLinkData.duration;
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

