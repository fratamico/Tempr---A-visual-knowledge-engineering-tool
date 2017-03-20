function showHeatmapPlot() {

  var margin = { top: 60, right: 10, bottom: 50, left: 400 },
  cellSize_width=215;
  cellSize_height=12;
  cellSize = 12;
  col_number=5;
  row_number=50;
  width = cellSize_width*col_number, // - margin.left - margin.right,
  height = cellSize_height*row_number , // - margin.top - margin.bottom,
  //gridSize = Math.floor(width / 24),
  colorBuckets = 11,
  legendElementWidth = cellSize_width*col_number/colorBuckets, //width of legend at bottom
  colors = ['#543005','#8c510a','#bf812d','#dfc27d','#f6e8c3','#ffffff','#c7eae5','#80cdc1','#35978f','#01665e','#003c30'];
  hcrow = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50], // change to gene name or probe id
  hccol = [1, 2, 3, 4, 5], // change to gene name or probe id
  rowLabel = get_heatmap_data()["ROW_LABELS"],
  colLabel = ['0%-20%','20%-40%','40%-60%','60%-80%','80%-100%'], // change to contrast name
  DOMAIN = get_heatmap_data()["DOMAIN"];


  d3.tsv("processing/heatmap_data.tsv",
    function(d) {
      return {
        row:   +d.row_idx,
        col:   +d.col_idx,
        value: +d.log2ratio
      };
    },
    function(error, data) {
      var colorScale = d3.scale.quantile()
      .domain([ DOMAIN[0] , 0, DOMAIN[DOMAIN.length-1]])
      .range(colors);

      var svg = d3.select("#chart").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
      ;
      var rowSortOrder=false;
      var colSortOrder=false;
      var rowLabels = svg.append("g")
      .selectAll(".rowLabelg")
      .data(rowLabel)
      .enter()
      .append("text")
      .text(function (d) { return d; })
      .attr("x", 0)
      .attr("y", function (d, i) { return hcrow.indexOf(i+1) * cellSize_height; })
      .style("text-anchor", "end")
      .attr("transform", "translate(-6," + cellSize_height / 1.5 + ")")
      .attr("class", function (d,i) { return "rowLabel mono r"+i;} ) 
      .on("mouseover", function(d) {d3.select(this).classed("text-hover",true);})
      .on("mouseout" , function(d) {d3.select(this).classed("text-hover",false);})
      .on("click", function(d,i) {rowSortOrder=!rowSortOrder; sortbylabel("r",i,rowSortOrder);d3.select("#order").property("selectedIndex", 4).node().focus();;})
      ;

      var colLabels = svg.append("g")
      .selectAll(".colLabelg")
      .data(colLabel)
      .enter()
      .append("text")
      .text(function (d) { return d; })
      .attr("x", 0)
      .attr("y", function (d, i) { return hccol.indexOf(i+1) * cellSize_width; })
      .style("text-anchor", "left")
      .attr("transform", "translate("+cellSize_width/2 + ",-6) rotate (-90)")
      .attr("class",  function (d,i) { return "colLabel mono c"+i;} )
      .on("mouseover", function(d) {d3.select(this).classed("text-hover",true);})
      .on("mouseout" , function(d) {d3.select(this).classed("text-hover",false);})
      .on("click", function(d,i) {colSortOrder=!colSortOrder;  sortbylabel("c",i,colSortOrder);d3.select("#order").property("selectedIndex", 3).node().focus();;})
      ;

  //colLabels.select("text") 
  //  .attr("transform", "rotate(-90)");

  var heatMap = svg.append("g").attr("class","g3")
  .selectAll(".cellg")
  .data(data,function(d){return d.row+":"+d.col;})
  .enter()
  .append("rect")
  .attr("x", function(d) { return hccol.indexOf(d.col) * cellSize_width; })
  .attr("y", function(d) { return hcrow.indexOf(d.row) * cellSize_height; }) //coloring of cells
  .attr("class", function(d){return "cell cell-border cr"+(d.row-1)+" cc"+(d.col-1);})
  .attr("width", cellSize_width)
  .attr("height", cellSize_height) //height of bottom cell
  .style("fill", function(d) { return colorScale(d.value); })
  .on("mouseover", function(d){
               //highlight text
               d3.select(this).classed("cell-hover",true);
               d3.selectAll(".rowLabel").classed("text-highlight",function(r,ri){ return ri==(d.row-1);});
               d3.selectAll(".colLabel").classed("text-highlight",function(c,ci){ return ci==(d.col-1);});

               //Update the tooltip position and value
               d3.select("#tooltip")
               .style("left", (d3.event.pageX+10) + "px")
               .style("top", (d3.event.pageY-10) + "px")
               .select("#value")
               .text("lables:"+rowLabel[d.row-1]+","+colLabel[d.col-1]+"\ndata:"+d.value);  
               //Show the tooltip
               d3.select("#tooltip").classed("hidden", false);
             })
  .on("mouseout", function(){
   d3.select(this).classed("cell-hover",false);
   d3.selectAll(".rowLabel").classed("text-highlight",false);
   d3.selectAll(".colLabel").classed("text-highlight",false);
   d3.select("#tooltip").classed("hidden", true);
 });

  var legend = svg.selectAll(".legend")
  .data([get_data_names()["GROUP_A_NAME"],DOMAIN[1],DOMAIN[2],DOMAIN[3],DOMAIN[4],DOMAIN[5],DOMAIN[6],DOMAIN[7],DOMAIN[8],DOMAIN[9],get_data_names()["GROUP_B_NAME"]]) //SIMILARLY PUT DOMAIN HERE
  .enter().append("g")
  .attr("class", "legend");

  legend.append("rect")
  .attr("x", function(d, i) { return legendElementWidth * i; })
  .attr("y", height+(cellSize*2))
  .attr("width", legendElementWidth)
  .attr("height", cellSize)
  .style("fill", function(d, i) { return colors[i]; });

  legend.append("text")
  .attr("class", "mono")
  .text(function(d) { return d; })
  .attr("width", legendElementWidth)
  .attr("x", function(d, i) { return legendElementWidth * i; })
  .attr("y", height + (cellSize*4));

// Change ordering of cells
function sortbylabel(rORc,i,sortOrder){
 var t = svg.transition().duration(3000);
 var log2r=[];
       var sorted; // sorted is zero-based index
       d3.selectAll(".c"+rORc+i) 
       .filter(function(ce){
        log2r.push(ce.value);
      })
       ;
       if(rORc=="r"){ // click action event (to change order of time intervals)
         sorted=d3.range(col_number).sort(function(a,b){ if(sortOrder){ return log2r[b]-log2r[a];}else{ return log2r[a]-log2r[b];}});
         t.selectAll(".cell")
         .attr("x", function(d) { return sorted.indexOf(d.col-1) * cellSize_width; })
         ;
         t.selectAll(".colLabel")
         .attr("y", function (d, i) { return sorted.indexOf(i) * cellSize_width; })
         ;
       }else{ // clict column (to change order of action events)
         sorted=d3.range(row_number).sort(function(a,b){if(sortOrder){ return log2r[b]-log2r[a];}else{ return log2r[a]-log2r[b];}});
         t.selectAll(".cell")
         .attr("y", function(d) { return sorted.indexOf(d.row-1) * cellSize_height; })
         ;
         t.selectAll(".rowLabel")
         .attr("y", function (d, i) { return sorted.indexOf(i) * cellSize_height; })
         ;
       }
     }


  // 
  var sa=d3.select(".g3")
  .on("mousedown", function() {
    if( !d3.event.altKey) {
     d3.selectAll(".cell-selected").classed("cell-selected",false);
     d3.selectAll(".rowLabel").classed("text-selected",false);
     d3.selectAll(".colLabel").classed("text-selected",false);
   }
   var p = d3.mouse(this);
   sa.append("rect")
   .attr({
     rx      : 0,
     ry      : 0,
     class   : "selection",
     x       : p[0],
     y       : p[1],
     width   : 1,
     height  : 1
   })
 })
  .on("mousemove", function() {
   var s = sa.select("rect.selection");

   if(!s.empty()) {
     var p = d3.mouse(this),
     d = {
       x       : parseInt(s.attr("x"), 10),
       y       : parseInt(s.attr("y"), 10),
       width   : parseInt(s.attr("width"), 10),
       height  : parseInt(s.attr("height"), 10)
     },
     move = {
       x : p[0] - d.x,
       y : p[1] - d.y
     }
     ;

     if(move.x < 1 || (move.x*2<d.width)) {
       d.x = p[0];
       d.width -= move.x;
     } else {
       d.width = move.x;       
     }

     if(move.y < 1 || (move.y*2<d.height)) {
       d.y = p[1];
       d.height -= move.y;
     } else {
       d.height = move.y;       
     }
     s.attr(d);

                 // deselect all temporary selected state objects
                 d3.selectAll('.cell-selection.cell-selected').classed("cell-selected", false);
                 d3.selectAll(".text-selection.text-selected").classed("text-selected",false);

                 d3.selectAll('.cell').filter(function(cell_d, i) {
                   if(
                     !d3.select(this).classed("cell-selected") && 
                         // inner circle inside selection frame 
                         (this.x.baseVal.value)+cellSize_width >= d.x && (this.x.baseVal.value)<=d.x+d.width && 
                         (this.y.baseVal.value)+cellSize_height >= d.y && (this.y.baseVal.value)<=d.y+d.height
                         ) {

                     d3.select(this)
                   .classed("cell-selection", true)
                   .classed("cell-selected", true);

                   d3.select(".r"+(cell_d.row-1))
                   .classed("text-selection",true)
                   .classed("text-selected",true);

                   d3.select(".c"+(cell_d.col-1))
                   .classed("text-selection",true)
                   .classed("text-selected",true);
                 }
               });
               }
             })
  .on("mouseup", function() {
            // remove selection frame
            sa.selectAll("rect.selection").remove();

             // remove temporary selection marker class
             d3.selectAll('.cell-selection').classed("cell-selection", false);
             d3.selectAll(".text-selection").classed("text-selection",false);
           })
  .on("mouseout", function() {
   if(d3.event.relatedTarget.tagName=='html') {
                 // remove selection frame
                 sa.selectAll("rect.selection").remove();
                 // remove temporary selection marker class
                 d3.selectAll('.cell-selection').classed("cell-selection", false);
                 d3.selectAll(".rowLabel").classed("text-selected",false);
                 d3.selectAll(".colLabel").classed("text-selected",false);
               }
             });
  });
}