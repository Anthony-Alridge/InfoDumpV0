var value;
function show_del_button(element) {
  var es = document.getElementById('del_button');
  es.style.display = 'table-cell';
  value = element;
}

function get_value(){
  console.log(value);
  return value;
}
