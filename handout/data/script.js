document.addEventListener('DOMContentLoaded', function(){
  var elements = document.getElementsByClassName('markdown');
  for (var index = 0; index < elements.length; index++) {
    var element = elements[index];
    element.innerHTML = marked(element.textContent);
  }
}, false);
