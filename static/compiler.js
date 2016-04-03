var Model = {
	codeContent : null,
	init : function(){
		this.codeContent = "";
	},
	setContent : function(content){
		this.codeContent = content;
	},
	getContent : function(){
		return this.codeContent;
	},
};

var Controller = {
	init : function(){
		Model.init();
		View.init();
	},
	runCode : function(){
		//var code = ;
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
		return document.getElementById("codeEditor").value;
	},
	setContent : function(content){
		document.getElementById("codeEditor").value = content;
	},
	getInput : function(){

	},
	setInput : function(){

	},
	setOutput : function(){

	}
};

