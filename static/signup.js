function signup(loginUrl , SignupUrl){

var myData = {
  "name" : $("#name").val() , 
  "username" : $("#username").val() , 
  "password" : $("#password1").val()
};

$.ajax({
    url: SignupUrl,
    type: "POST",
    dataType: "json",
    contentType: 'application/json; charset=utf-8',
    data :  JSON.stringify(myData),
    success: function(resultData) {
      //alert(resultData["status"]);

      if (resultData["status"] == "success"){
        window.location = window.location.protocol + "//" + window.location.host + loginUrl;
      }
      else{
        $("#mssg").text(resultData["message"]);
      }
    },
    error : function(jqXHR, textStatus, errorThrown) {
      alert("ajax error");
      console.log(jqXHR);
      console.log(textStatus);
      console.log(errorThrown);
    }
});
}