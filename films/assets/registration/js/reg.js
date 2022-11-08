jQuery(document).ready(function($) {
    var hint = $('.hint');
    $('input.pass1').on({
    mouseenter: function () {
        hint.toggleClass('hide');
    },
    mouseleave: function () {
        hint.toggleClass('hide');
    }});

    const btnWrap = $('.btn-wrap');
    const menu = $('.alert');
    const bar = $('.bar');
    window.setTimeout(function() {
      menu.toggleClass('active2');
      window.setTimeout(function() {
          menu.toggleClass('active2');
      }, 3000);
      bar.toggleClass('spanFill');
    }, 200);
});
