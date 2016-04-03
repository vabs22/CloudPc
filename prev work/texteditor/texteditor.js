var Model = {
	fileContent : null,
	fileName : null,
	init : function(){
		this.fileName = "New Untitled";
		this.fileContent = "";
	},
	setContent : function(content){
		this.fileContent = content;
	},
	setName : function(name){
		this.fileName = name;
	},
	getContent : function(){
		return this.fileContent;
	},
	getName  :function(){
		return this.fileName;
	}
};

var Controller = {
	init : function(){
		Model.init();
		View.init();
		var title = Model.getName();
		View.setTitle(title);
		console.log(title);
	},
	saveClick : function(){
		var content = View.getContent();
		Model.setContent(content);
	},
	newFile : function(){

	},
	openFile : function(){

	},
	saveAsFile : function(){

	}
};

var View = {
	myCodeMirror : null,
	init : function(){
		this.myCodeMirror = CodeMirror.fromTextArea(document.getElementById("codeEditor"), {
			value: "Type code here",
			mode: "javascript",
			lineNumbers: true,
			theme: "monokai",
		});
	},
	getContent : function(){

	},
	setContent : function(content){

	},
	setTitle : function(title){
		document.title = title;
	}
};

