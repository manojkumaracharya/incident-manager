window.$ = window.jQuery = require('jquery');

function logout() {
  localStorage.setItem("",username);
  window.location="index.html";
}

$(document).ready(function () {
    //https://stackoverflow.com/questions/27765666/passing-variable-through-javascript-from-one-html-page-to-another-page
    document.getElementById("username").innerHTML = localStorage.getItem("username");

    $('#mainContent').height($(window).height());

    $('a').click(function(e) {
        e.preventDefault();
        $('#mainContent').height('0px');
        $("#mainContent").load($(this).attr('href'));
        $("#mainContent").css({"margin-left":"160px","position":"absolute"});
      });
});