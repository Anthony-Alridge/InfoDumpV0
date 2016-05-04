//JavaScript to interact with focus page

//A collection of methods which toggle the show hide status of elements on the page
function hideContent(element_hide,element_show) {
  var eh = document.getElementById(element_hide);
  var es = document.getElementById(element_show);
  eh.style.display = 'none';
  es.style.display = 'table-cell';
}
