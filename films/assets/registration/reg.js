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
    console.log(bar);
    window.setTimeout(function() {
      menu.toggleClass('active2');
      window.setTimeout(function() {
          menu.toggleClass('active2');
      }, 3000);
      bar.toggleClass('spanFill');
    }, 200);



//    var counter1 = 0;
//    var counter2 = 0;
//    (function timeout1() {
//      console.log('counter1', counter1);
//      counter1++;
//      var i = 0;
//      (function timeout2() {
//        console.log('counter2', counter2);
//        counter2++;
//        ++i;
//        setTimeout(i < 4 ? timeout2 : timeout1, 1000);
//      })();
//    })();
//
//    (function show() {
//      left += 1;
//      alert.css('left', left);
//      if (left >= 0) {
//
//      }
//    })
  // let anim = setInterval(function() {
  //   show();
  // }, 5);
  //
  // var loading = function() {
  //
  //     value += 1;
  //     progressbar.width(value+'%');
  //
  //     // $('.progress-value').html(value + '%');
  //     console.log(value);
  //
  //     if (value >= max) {
  //         clearInterval(l);
  //     }
  // };
  //
  // function show() {
  //   left += 1
  //   alert.css('left', left);
  //
  //   if (left >= 0) {
  //     clearInterval(anim);
  //     // var l = setInterval(loading, 25);
  //   };
  // }

//     var showMes = function() {
//         left += 1;
//         alert.css('left', left);
//
//         if (left==0) {
//           clearInterval(anim);
//         }
//     };
//
//
//     // var anim = setInterval(function() {
//     //   showMes();
//     // }, 200);
//
//     var animate = setInterval(function() {
//         showMes();
//         anim = setInterval(loading, 200);
//     }, 200);
});
