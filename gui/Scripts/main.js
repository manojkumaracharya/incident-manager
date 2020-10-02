window.$ = window.jQuery = require('jquery');
var {PythonShell} = require('python-shell');
var path = require("path");
var jsonOutput = '';

function faceDetection(){
  var options = {
    scriptPath : path.join(__dirname, '/../engine/'),
    args : ['getData']
  }
  //alert(options)
  //https://github.com/neha01/FaceRecognition
  //https://www.youtube.com/watch?v=h21wMKGs0qs&feature=youtu.be
  var pyshell = new PythonShell('videoTester.py', options);
  //alert(pyshell)
  var jsonOutput = ''
  pyshell.on('message', function(message) {
    jsonOutput += message;
  })

  pyshell.end(function (err) {
    if (err) throw err;
    console.log(jsonOutput)
    var output = JSON.parse(jsonOutput);
    console.log(output)
    if(output == "Face Recognized"){
      window.location="tabs.html";
      return
    }
  });
}

function login() {
  var username = document.getElementById("username").value;
  var password = document.getElementById("password").value;
  var message = '';
  window.location="tabs.html";
  return;

  if(username && password){
    console.log(username);
    var userDetails = JSON.parse(jsonOutput);
    for(var i =0;i<userDetails.length;i++){
      if(userDetails[i].members_uname == username ){
        if(userDetails[i].member_password == password){
          message = "login successful"
          localStorage.setItem("username",userDetails[i].members_real_name);
          //https://stackoverflow.com/questions/48493102/javascript-load-an-html-page-with-button-click
          window.location="tabs.html";
        }
        else{
          message = "Invalid user id and/or password"
        }
      }
    }
  }else{
    message = 'Please enter valid login credentials';    
  }  

  if(message == ''){
    document.getElementById("message").innerHTML = "user not registered";
  }else{
    document.getElementById("message").innerHTML = message;
  }
  return
  // localStorage.setItem("username",username);
  // window.location="tabs.html";
  
  //var getInput = prompt("Hey type something here: "); 
}

//https://websitesetup.org/bootstrap-tutorial-for-beginners/
$(document).ready(function(){
  $('.header').height($(window).height());
  getUserData();
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