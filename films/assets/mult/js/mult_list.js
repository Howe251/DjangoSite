$(document).ready(function(){
var $element = $('.container');
$(window).scroll(function() {
  var scroll = $(window).scrollTop() + $(window).height();
  var offset = $element.offset().top + $element.height();
  if (scroll >= offset) {
    $('.bottom').addClass('fixed');
  }
  else if (scroll <= offset) {
    $('.bottom').removeClass('fixed');
  }
});
});