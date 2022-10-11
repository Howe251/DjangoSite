jQuery(document).ready(function($) {
  var rb = $('.r');
  var cab = $('.cab_list');
  $('.cab_list').click(function(event) {
    cab.each(function(index, el) {
      $(el).removeClass('selected');
    });
    $(this).toggleClass('selected');
    var clicked = this.classList[1]
    rb.each(function(index, el) {
      $(el).removeClass('active');
      if ($(el).hasClass(clicked)) $(el).addClass('active');
    });
  });
})
