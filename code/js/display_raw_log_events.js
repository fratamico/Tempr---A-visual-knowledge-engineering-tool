function display_raw_log_events() {
  all_actionevents = get_raw_log_events(); 
  
  var parent_ul = document.getElementById("filterable_list_ul");

  for (var i = 0; i < all_actionevents.length; i++) {
  	var new_li = document.createElement('li');

  	var new_input = document.createElement('input');
  	new_input.setAttribute("type", "checkbox");
  	new_input.setAttribute("name", "aca");
  	new_input.setAttribute("value", all_actionevents[i]);

  	new_li.appendChild(new_input)
  	new_li.appendChild(document.createTextNode(" " + all_actionevents[i]))

  	parent_ul.appendChild(new_li);
  }
}