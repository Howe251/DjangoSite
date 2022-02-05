document.addEventListener("DOMContentLoaded", function(){
  var div = Array.prototype.slice.call(document.querySelectorAll('#content-main'),0)[0];
  var dropdownArray = Array.prototype.slice.call(div.querySelectorAll('.module:not(.aligned) > h2'),0);

    dropdownArray.forEach(function(el) {
      el.parentElement.classList.add('dropdown', 'hide2')
      var button = el,
          menu = el.parentElement.querySelector('table');
      if (menu) {
        menu.classList.add("hide");
        var td = menu.querySelectorAll('.field-name');
        if (td) {
          td.forEach((item) => {
            item.children[0].children[0].classList.add("selection");
          });
        }
      }

      button.onclick = function(event) {
        if (!menu.hasClass('show')){
          button.parentElement.classList.add('show');
          button.parentElement.classList.remove('hide2');
          menu.classList.add('show');
          menu.classList.remove('hide');
          event.preventDefault();
        }
        else {
          button.parentElement.classList.add('hide2');
          button.parentElement.classList.remove('show');
          menu.classList.remove('show');
          menu.classList.add('hide');
          event.preventDefault();
        }
      }
  });

Element.prototype.hasClass = function(className) {
    return this.className && new RegExp("(^|\\s)" + className + "(\\s|$)").test(this.className);
};
});
