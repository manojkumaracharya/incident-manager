window.$ = window.jQuery = require('jquery');
var {PythonShell} = require('python-shell');
var path = require("path");
var jsonOutput = '';

function faceDetection(){
  window.location="video.html";
}

function login() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  var message = '';
  //console.log(username);
  // var userDetails = JSON.parse(jsonOutput);
  // for(var i =0;i<userDetails.length;i++){
  //   if(userDetails[i].userid == username ){
  //     if(userDetails[i].password == password){
  //       message = "login successful"
  //       localStorage.setItem("username",userDetails[i].username);
  //        //https://stackoverflow.com/questions/48493102/javascript-load-an-html-page-with-button-click
  //       window.location="tabs.html";
  //     }
  //     else{
  //       message = "Invalid user id and/or password"
  //     }
  //   }
  // }
  // localStorage.setItem("username",userDetails[i].username);
  // window.location="tabs.html";

  // if(message == ''){
  //   document.getElementById("message").innerHTML = "user not registered";
  // }else{
  //   document.getElementById("message").innerHTML = message;
  // }

  localStorage.setItem("username",username);
  window.location="tabs.html";
  
  //var getInput = prompt("Hey type something here: "); 
}

//https://websitesetup.org/bootstrap-tutorial-for-beginners/
$(document).ready(function(){
  $('.header').height($(window).height());
  //getUserData();
})

function getUserData() {
  var options = {
    scriptPath : path.join(__dirname, '/../engine/'),
    args : ['getUserData']
  }
  //alert(options)
  var pyshell = new PythonShell('Hackademy_Incident_Management.py', options);
  //alert(pyshell)
  
  pyshell.on('message', function(message) {
    jsonOutput += message;
  })

  pyshell.end(function (err) {
    if (err) throw err;
    //console.log('finished');
    console.log(jsonOutput);
  });
}