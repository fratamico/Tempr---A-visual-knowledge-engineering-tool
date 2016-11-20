function showTemporalPlot(NUM_SPLITS) {
  var to_display = $("input:checkbox[name=aca]:checked").map(function(){return $(this).val()}).get();

  //uncheck all boxes
  var cbarray = document.getElementsByName("aca");
  for(var i = 0; i < cbarray.length; i++){
    cbarray[i].checked = false;
  };

  //create divs where plots will go
  var plots_container = document.getElementById('plots_container');

  // remove all current children
  plots_container.innerHTML = '';

  for (var i in to_display) {
    var merged_action_list = [for (e of document.getElementsByClassName(to_display[i] + "_mergedActionList")) e.textContent];
    var plot_title = document.createElement('p');
    if (merged_action_list.length === 0) {
      var bold_element = document.createElement("b");
      bold_element.appendChild(document.createTextNode(to_display[i]));
      plot_title.appendChild(bold_element);
    } else {
      var bold_element = document.createElement("b");
      bold_element.appendChild(document.createTextNode(to_display[i] + ": "));
      plot_title.appendChild(bold_element);
      
      plot_title.appendChild(document.createElement("br"));
      
      var merged_action_list_node = document.createTextNode(merged_action_list.join(" + "));
      var span = document.createElement('span');
      span.style.fontSize = "11px";
      span.style.display="block";
      span.style.lineHeight = "1.2";
      span.appendChild(merged_action_list_node);
      plot_title.appendChild(span);
    }

    plots_container.appendChild(plot_title);

    var plot_chart = document.createElement('div');
    plot_chart.setAttribute("id", "chart_" + to_display[i].split(".").join("_").split(" ").join("_"));
    plot_chart.setAttribute("class", "stacked_charts");

    plots_container.appendChild(plot_chart);

    //create_graph(to_display[i], merged_action_list);
    create_quartile_graph(NUM_SPLITS, to_display[i], merged_action_list);
  }
}

function addArrays(ar1, ar2){
    var ar3 = [];
    for(var i in ar1)
        ar3.push(ar1[i] + ar2[i]);
    return ar3;
}

function create_quartile_graph(NUM_SPLITS, action_item, merged_action_list) {
var action_item_new_name = action_item.split(".").join("_").split(" ").join("_");
var margin = {top: 10, right: 50, bottom: 50, left: 40},
    width = 830 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;


d3.json("processing/json_files/ALL_ACTIONS_" + NUM_SPLITS + ".json", function(error, orig_data) {
  var data = {
    "timeslice": [],
    "freq_difference": []
  };

  var high_25 = [];
  var high_50 = [];
  var high_75 = [];
  var low_25 = [];
  var low_50 = [];
  var low_75 = [];

  for (i=0; i<=NUM_SPLITS; i++) {
  	high_25.push({x: i*(100/NUM_SPLITS), y: 0});
  	high_50.push({x: i*(100/NUM_SPLITS), y: 0});
  	high_75.push({x: i*(100/NUM_SPLITS), y: 0});
  	low_25.push({x: i*(100/NUM_SPLITS), y: 0});
  	low_50.push({x: i*(100/NUM_SPLITS), y: 0});
  	low_75.push({x: i*(100/NUM_SPLITS), y: 0});
  }

  if (merged_action_list.length !== 0) {
  	for (var i = 0; i < NUM_SPLITS; i++) {
	  	var merged_freq_list_high = [];
	  	var merged_freq_list_low = [];

	    for (var j = 0; j < get_num_users()["Low"]; j++) {
	      merged_freq_list_low.push(0);
	    }

	    for (var j = 0; j < get_num_users()["High"]; j++) {
	      merged_freq_list_high.push(0);
	    }
	    
	    for (var ind=0; ind < merged_action_list.length; ind++){
	    	merged_freq_list_high = addArrays(merged_freq_list_high, orig_data["High"][i.toString()][merged_action_list[ind]]);
	    	merged_freq_list_low = addArrays(merged_freq_list_low, orig_data["Low"][i.toString()][merged_action_list[ind]]);
	    }

	    high_25[i].y = math.quantileSeq(merged_freq_list_high, 0.25);
        high_50[i].y = math.quantileSeq(merged_freq_list_high, 0.5);
        high_75[i].y = math.quantileSeq(merged_freq_list_high, 0.75);
        low_25[i].y = math.quantileSeq(merged_freq_list_low, 0.25);
        low_50[i].y = math.quantileSeq(merged_freq_list_low, 0.5);
        low_75[i].y = math.quantileSeq(merged_freq_list_low, 0.75);
	}
  } else {
    for (var i = 0; i < NUM_SPLITS; i++) {
      high_25[i].y = math.quantileSeq(orig_data["High"][i.toString()][action_item], 0.25);
      high_50[i].y = math.quantileSeq(orig_data["High"][i.toString()][action_item], 0.5);
      high_75[i].y = math.quantileSeq(orig_data["High"][i.toString()][action_item], 0.75);
      low_25[i].y = math.quantileSeq(orig_data["Low"][i.toString()][action_item], 0.25);
      low_50[i].y = math.quantileSeq(orig_data["Low"][i.toString()][action_item], 0.5);
      low_75[i].y = math.quantileSeq(orig_data["Low"][i.toString()][action_item], 0.75);
    };
  }

  //last one is same as one before for step function to look right
    high_25[high_25.length-1].y = high_25[high_25.length-2].y
    high_50[high_50.length-1].y = high_50[high_50.length-2].y
    high_75[high_75.length-1].y = high_75[high_75.length-2].y
    low_25[low_25.length-1].y = low_25[low_25.length-2].y
    low_50[low_50.length-1].y = low_50[low_50.length-2].y
    low_75[low_75.length-1].y = low_75[low_75.length-2].y

	var xScale = d3.scale.linear()
	    .domain([0, 100])
	    .range([0, width]);

	//MAX Y VALUE
	max_y_low_75 = d3.max(low_75, function(d){ return d.y; });
	max_y_high_75 = d3.max(high_75, function(d){ return d.y; });

	var yScale = d3.scale.linear()
	    .domain([0, d3.max([max_y_low_75, max_y_high_75])])
	    .range([height, 0]);

	var xAxis = d3.svg.axis()
	    .scale(xScale)
	    .orient("bottom")
	    .outerTickSize(0)
	    .tickPadding(10)
	    .tickFormat(function(d) { return d + "%"; });

	var yAxis = d3.svg.axis()
	    .scale(yScale)
	    .orient("left")
	    .innerTickSize(-width)
	    .outerTickSize(0)
	    .tickPadding(10);

	var line = d3.svg.line()
	    .interpolate("step-after")
	    .x(function(d) { return xScale(d.x); })
	    .y(function(d) { return yScale(d.y); });

	var svg = d3.select("#chart_" + action_item_new_name).append("svg")
	    .attr("width", width + margin.left + margin.right)
	    .attr("height", height + margin.top + margin.bottom)
	    .append("g")
	    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	  svg.append("g")
	      .attr("class", "x axis")
	      .attr("transform", "translate(0," + height + ")")
	      .call(xAxis)

	  svg.append("g")
	      .attr("class", "y axis")
	      .call(yAxis)


	  //shade area between HL lines
	  var area_high = d3.svg.area()
	      .interpolate("step-after")
	      .x( function(d) { return xScale(high_25[d].x) } )
	      .y0( function(d) { return yScale(high_25[d].y) } )
	      .y1(  function(d) { return yScale(high_75[d].y) } );
	  svg.append('path')
	      .datum(d3.range(high_25.length))
	      .style("fill", "#35978f")
	      .style("fill-opacity", .3)
	      .attr('class', 'area')
	      .attr('d', area_high);

	   //shade area between LL lines
	    var area_low = d3.svg.area()
	      .interpolate("step-after")
	      .x( function(d) { return xScale(low_25[d].x) } )
	      .y0( function(d) { return yScale(low_25[d].y) } )
	      .y1(  function(d) { return yScale(low_75[d].y) } );
	    svg.append('path')
	      .datum(d3.range(low_25.length))
	      .style("fill", "#bf812d")
	      .style("fill-opacity", .3)
	      .attr('class', 'area')
	      .attr('d', area_low);

	  
	  //High Learners
	  //Lines
	  svg.append("path")
	      .data([high_50])
	      .attr("class", "line")
	      .attr("d", line)
	      .style("stroke-dasharray", ("3, 3")) //dashed line
	      .attr('stroke-width', 3) // width of line
	      .attr('stroke', "#01665e"); 
	  /*svg.append("path")
	      .data([high_25])
	      .attr("class", "line")
	      .attr("d", line)
	      .style("stroke-dasharray", ("3, 3"))
	      .attr('stroke-width', 2) // width of line
	      .attr('stroke', "#35978f"); 
	  svg.append("path")
	      .data([high_75])
	      .attr("class", "line")
	      .attr("d", line)
	      .style("stroke-dasharray", ("3, 3"))
	      .attr('stroke-width', 2) // width of line
	      .attr('stroke', "#35978f"); */
	   //HL line label
	  svg.append("text")
	      .attr("transform", "translate(" + (width+3) + "," + yScale(high_50[high_50.length-1].y) + ")") //replace 2 with last value
	      .attr("dy", ".35em")
	      .attr("text-anchor", "start")
	      .style("fill", "#01665e")
	      .text(get_data_names()["GROUP_B_NAME"]);

	  

	  //Low Learners
	  svg.append("path")
	      .data([low_50])
	      .attr("class", "line")
	      .attr("d", line)
	      .style("stroke-dasharray", ("3, 3")) //dashed line
	      .attr('stroke-width', 3) // width of line
	      .attr('stroke', "#8c510a"); 
	  /*svg.append("path")
	      .data([low_25])
	      .attr("class", "line")
	      .attr("d", line)
	      .style("stroke-dasharray", ("3, 3")) //dashed line
	      .attr('stroke-width', 2) // width of line
	      .attr('stroke', "#bf812d"); 
	   svg.append("path")
	      .data([low_75])
	      .attr("class", "line")
	      .attr("d", line)
	      .style("stroke-dasharray", ("3, 3")) //dashed line
	      .attr('stroke-width', 2) // width of line
	      .attr('stroke', "#bf812d"); */

	   //LL line label
	   svg.append("text")
	      .attr("transform", "translate(" + (width+3) + "," + yScale(low_50[low_50.length-1].y) + ")") //replace 2 with last value
	      .attr("dy", ".35em")
	      .attr("text-anchor", "start")
	      .style("fill", "#8c510a")
	      .text(get_data_names()["GROUP_A_NAME"]);

	    
});

}