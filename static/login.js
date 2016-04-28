function login(HomeUrl , LoginUrl){

var myData = {
  "username" : $("#username").val() , 
  "password" : $("#password").val()
};

$.ajax({
    url: LoginUrl,
    type: "POST",
    dataType: "json",
    contentType: 'application/json; charset=utf-8',
    data :  JSON.stringify(myData),
    success: function(resultData) {
      //alert(resultData["status"]);

      if (resultData["status"] == "success"){
        window.location = window.location.protocol + "//" + window.location.host + HomeUrl;
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