window.$ = window.jQuery = require('jquery');

function login() {
  var username = document.getElementById("username").value;
  //console.log(username);

  //var getInput = prompt("Hey type something here: ");
  localStorage.setItem("username",username);

  //https://stackoverflow.com/questions/48493102/javascript-load-an-html-page-with-button-click
  window.location="tabs.html";
}

//https://websitesetup.org/bootstrap-tutorial-for-beginners/
$(document).ready(function(){
  $('.header').height($(window).height());
})