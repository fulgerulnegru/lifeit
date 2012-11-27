$(document).ready(function(){

  $('.under').toggle(function(){
    $(this).next().show();
    return false;
  },function(){
    $(this).next().hide();
    return false;
  });

  $('.win-command-m').toggle(function(){
    $(".well-css").animate({height: "toggle", opacity: "toggle"});
  },function(){
    $('.well-css').hide();
  });

});
