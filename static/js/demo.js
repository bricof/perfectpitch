
var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 750 - margin.left - margin.right,
    height = 250 - margin.top - margin.bottom;

var x=[0,0], y=[0,0], xAxis=[0,0], yAxis=[0,0], line=[0,0], svg=[0,0];
var xLabel = ["time(s)*44100","frequency"];
var yLabel = ["pressure","normalized amplitude"];

for (var i=0; i<2; i++) {

  x[i] = d3.scale.linear()
      .range([0, width]);
  
  y[i] = d3.scale.linear()
      .range([height, 0]);
  
  xAxis[i] = d3.svg.axis()
      .scale(x[i])
      .orient("bottom");
  
  yAxis[i] = d3.svg.axis()
      .scale(y[i])
      .orient("left");

}

x[0].domain([0,1024]);
y[0].domain([-10000,10000]);

x[1].domain([0,4300]);
y[1].domain([-0.1,1.1]);


line[0] = d3.svg.line()
    .x(function(d) { return x[0](d.x); })
    .y(function(d) { return y[0](d.y); });

line[1] = d3.svg.line()
    .x(function(d) { return x[1](d.x); })
    .y(function(d) { return y[1](d.y); });

  
for (var i=0; i<2; i++) {

  svg[i] = d3.select("#chart" + i).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
  
  svg[i].append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis[i])
    .append("text")
      .attr("x", width)
      .attr("y", 0)
      .style("text-anchor", "end")
      .style("font", "14px sans-serif")
      .text(xLabel[i]);
  
  svg[i].append("g")
      .attr("class", "y axis")
      .call(yAxis[i])
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .style("font", "14px sans-serif")
      .text(yLabel[i]);

}  


  
var onTimerTick = function() {

  d3.json('/api/0', function(error, data) {
  
    data.forEach(function(d) {
      d.x = +d.x;
      d.y = +d.y;
    });
    
    var lines0 = svg[0].selectAll(".line")
                     .data([data[0]]);
    
    lines0.enter()
      .append("path")
        .attr("class", "line")
        .attr("d", line[0]);

    lines0
      .transition()
        .duration(200)
        .attr("d", line[0]);

    var lines1 = svg[1].selectAll(".line")
                     .data([data[1]]);
    
    lines1.enter()
      .append("path")
        .attr("class", "line")
        .attr("d", line[1]);

    lines1
      .transition()
        .duration(200)
        .attr("d", line[1]);
    
    
    $( "#notePrediction" ).html(data[2]);
    
    return onTimerTick();

  });

};


$(function() {
  onTimerTick();
});


