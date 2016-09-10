function create_graph(action_item, merged_action_list) {
  var action_item_new_name = action_item.split(".").join("_").split(" ").join("_");
var margin = {top: 50, right: 50, bottom: 50, left: 50},
    width = 890 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

var chart = d3_horizon()
    .width(width)
    .height(height)
    .bands(1)
    .mode("mirror")
    .interpolate("step-before"); //options: basis, monotone, step-before, linear, etc. basis was default



var x = d3.scale.ordinal()
    .domain([, "5%", "10%", "15%", "20%", "25%", "30%", "35%", "40%", "45%", "50%", "55%", "60%", "65%", "70%", "75%", "80%", "85%", "90%", "95%", "100%"])
    .rangePoints([0, width]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var svg = d3.select("#chart_" + action_item_new_name).append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)



d3.json("processing/json_files/ALL_ACTIONS_FREQUENCY.json", function(error, orig_data) {
  var data = {
    "timeslice": [],
    "freq_difference": []
  };

  if (merged_action_list.length !== 0) {
    for (var i = 1; i <= 20; i++) {
      data.timeslice.push(i);
      data.freq_difference.push(0);
    };
    for (var ind=0; ind < merged_action_list.length; ind++){
      for (var i = 1; i <= 20; i++) {
        data.freq_difference[i-1] += parseFloat(orig_data[merged_action_list[ind]][i - 1]);
      };
    };
  } else {
    for (var i = 1; i <= 20; i++) {
      data.timeslice.push(i);
      data.freq_difference.push(parseFloat(orig_data[action_item][i - 1]));
    };
  }

  var max_of_array = Math.max.apply(Math, data.freq_difference);

  var y1 = d3.scale.linear().domain([0, max_of_array]).range([180, 0]);


  var yAxisRight = d3.svg.axis().scale(y1)
      .orient("right").ticks(5);

  // Transpose column values to rows.
  data = data.freq_difference.map(function(freq_difference, i) {
    return [data.timeslice[i], freq_difference];
  });

  // Render the chart.
  svg.data([data]).call(chart);

  svg.append("g")
    .attr("class", "axis")
    .attr("transform", "translate(0," + (height) + ")")
    .call(xAxis);

  svg.append("g")       
    .attr("class", "y axis")  
    .attr("transform", "translate(" + width + " ,20)") 
    .call(yAxisRight);

});

}



