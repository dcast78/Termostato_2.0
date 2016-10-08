---
title: Grafici
process:
    markdown: true
    twig: true
---

<a href=termo/grafico.php style="font-family: Helvetica Neue, HelveticaNeue-Light, Helvetica Neue Light, Helvetica, Arial, Lucida Grande, sans-serif; font-weight: 400; font-size:1.5em;">Ingrandisci il grafico</a>

<div id=graph width="100%" height=100% style="border: 1px solid; text-align:center;">
</div>

{assets:inline_css}
body {
  font: 14px sans-serif;
}

.axis path,
.axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}


.line {
  fill: none;
  stroke: steelblue;
  stroke-width: 1.5px;
}
.overlay {
  fill: none;
  pointer-events: all;
}
.focus circle {
  fill: none;
  stroke: steelblue;
}
{/assets}
{assets:js order:10}
../../../0/termo/d3.v3.js
{/assets}
{assets:inline_js}
function append_chart() {
var margin = {top: 40, right: 60, bottom: 30, left: 50} ,
    width = parseInt(d3.select("#graph").style("width"))  - margin.left - margin.right,
    height = width/3;

//var width = parseInt(d3.select("#graph").style("width")) - margin.left - margin.right;
//var height = parseInt(d3.select("#graph").style("height")) - margin.top - margin.bottom;
//var height=400;

var parseDate = d3.time.format("%Y%m%d%H%M%S").parse,
    bisectDate = d3.bisector(function(d) { return d.date; }).left,
    formatValue = d3.format(",.2f"),
    formatTemp = function(d) { return formatValue(d) + "°C"; };

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var color = d3.scale.category10();

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .interpolate("basis")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.temperature); });

var svg = d3.select("#graph").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.tsv("termo/data.php" , function(error, data) {
  if (error) throw error;

  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));

  data.forEach(function(d) {
    d.date = parseDate(d.date);
  });

  var temps = color.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(d) {
        return {date: d.date, temperature: +d[name]};
      })
    };
  });

  x.domain(d3.extent(data, function(d) { return d.date; }));

  y.domain([
    d3.min(temps, function(c) { return d3.min(c.values, function(v) { return v.temperature; }); }),
    d3.max(temps, function(c) { return d3.max(c.values, function(v) { return v.temperature; }); })
  ]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Temperature (ºC)");

  var temp = svg.selectAll(".temp")
      .data(temps)
    .enter().append("g")
      .attr("class", "temp");

  temp.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", function(d) { return color(d.name); });

  temp.append("text")
      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.temperature) + ")"; })
      .attr("x", 3)
      .attr("dy", ".35em")
      .text(function(d) { return d.name; });

// New

  var focus = svg.append("g")
      .attr("class", "focus")
      .style("display", "none");

  focus.append("circle")
      .attr("r", .1);

  focus.append("text")
      .attr("x", 9)
      .attr("dy", ".35em");

  svg.append("rect")
      .attr("class", "overlay")
      .attr("width", width)
      .attr("height", height)
      .on("mouseover", function() { focus.style("display", null); })
      .on("mouseout", function() { focus.style("display", "none"); })
      .on("mousemove", mousemove);

  function mousemove() {
    var x0 = x.invert(d3.mouse(this)[0]),
        i = bisectDate(data, x0, 1),
        d0 = data[i - 1],
        d1 = data[i],
        d = x0 - d0.date > d1.date - x0 ? d1 : d0;
    focus.attr("transform", "translate(" + x(d.date) + ", -20 )");
    focus.select("text").text(formatTemp(d.setpoint));
  }
});
}
{/assets}
{assets:inline_js}
jQuery(document).ready( function() 
{
    append_chart();
});
{/assets}
