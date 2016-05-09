

function show_del_button(id) {
  var delete_button = document.getElementById(id);
  delete_button.style.display = 'block';
}
function hide_del_button(id) {
  var delete_button = document.getElementById(id);
  var del_button_hover = false;
  delete_button.addEventListener('mouseenter', function() {
    delete_button.style.display = 'block';
  })
  delete_button.addEventListener('mouseout', function() {
    delete_button.style.display = 'none';
  })
  if(!del_button_hover){
  delete_button.style.display = 'none';
}
}
