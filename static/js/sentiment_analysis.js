// set the dimensions and margins of the graph
var margin = {top: 30, right: 30, bottom: 30, left: 50},
    width = 460 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
var svg = d3.select("#sentiment_viz")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");



var score_list_data_ = document.getElementById("sentiment_score_list").textContent;
score_list_data_ = score_list_data_.split(",");
var score_list_data = []; 
for (var i=0, len=score_list_data_.length; i<len;i++){
  score_list_data.push(parseFloat(score_list_data_[i]));
}

// var score_list_data = [94.0, 145.0, 251.0, 218.0, 265.0, 98.0, 66.0, 80.0, 52.0, 63.0, 92.0, 80.0, 228.0, 91.0, 58.0, 91.0, 101.0,]
// var score_list_data = [0.2, 0.2, 0.2, 0.4, 0.6, 0.6, 0.1 ,0.2, 0.1,  0.4,0.2, 0.9]

var score_dict = document.getElementById("sentiment_score_dict").textContent;
score_dict = JSON.parse(score_dict);


var Nbin = 20; 



// Add X axis
var x = d3.scaleLinear()
  .domain([-1.0, 1.0])
  .range([ 0, width]);

var histogram = d3.histogram()
                  .domain(x.domain())
                  .thresholds(x.ticks(Nbin))
var bins = histogram(score_list_data)

svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x))
  .selectAll("text")
    .attr("transform", "translate(-10,0)rotate(-45)")
    .style("text-anchor", "end");

// Y axis
var y = d3.scaleBand()
  .range([ 0, height ])
  .domain([0, d3.max(bins, function(d) { return d.length;})])
  .padding(1);
svg.append("g")
  .call(d3.axisLeft(y))


// Lines
svg.selectAll("myline")
  .data(bins)
  .enter()
  .append("line")
    .attr("x1", function(d) { return x(d.Value); })
    .attr("x2", x(0))
    .attr("y1", function(d) { return y(d.Country); })
    .attr("y2", function(d) { return y(d.Country); })
    .attr("stroke", "grey")

// Circles
svg.selectAll("mycircle")
  .data(data)
  .enter()
  .append("circle")
    .attr("cx", function(d) { return x(d.Value); })
    .attr("cy", function(d) { return y(d.Country); })
    .attr("r", "4")
    .style("fill", "#69b3a2")
    .attr("stroke", "black")







// add the x Axis
/*
var x = d3.scaleLinear()
          .domain([-100,100])
          .range([0, width]);
svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x));

// add the y Axis
var y = d3.scaleLinear()
          .range([height, 0])
          .domain([0, 0.12]);
svg.append("g")
    .call(d3.axisLeft(y));

var x = d3.scaleLinear()
          .range([0, width])
          .domain([0, 0.12])
svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))

var y = d3.scaleLinear()
          .range([height, 0])
          .domain([-100, 100])
svg.append("g")
   .call(d3.axisLeft(y))

// Compute kernel density estimation
var kde = kernelDensityEstimator(kernelEpanechnikov(7), x.ticks(60));
var density =  kde(score_list_data); 


var tooltip = d3.select("#sentiment_viz")
                .append("div")
                .style("opacity", 0)
                .attr("class", "tooltip")
                .style("background-color", "black")
                .style("color", "white")
                .style("padding", "10px")

var showTooltip = function(d, i) { 
    tooltip
      .transition()
      .duration(100)
      .style("opacity", 1)
    
    tooltip
      .html()
      .style("left", (d3.mouse(this)[0] + 20) + "px")
      .style("top", (d3.mouse(this)[1]) + "px")
}

var moveTooltip = function(d, i) {
  tooltip
      .style("left", (d3.mouse(this)[0] + 20) + "px")
      .style("top", (d3.mouse(this)[1]) + "px")
}


var hideTooltip = function(d){
  tooltip
    .transition()
    .duration(100)
    .style("opacity", 0)
 } 




// Plot the area
svg.append("path")
    .attr("class", "path")
    .datum(density)
    .attr("fill", "#69b3a2")
    .attr("opacity", ".8")
    .attr("stroke", "#000")
    .attr("stroke-width", 1)
    .attr("stroke-linejoin", "round")
    .attr("d",  d3.line()
      .curve(d3.curveBasis)
        .x(function(d) { return x(d[0]); })
        .y(function(d) { return y(d[1]); })
    )
    .on("mouseover", showTooltip)
    .on("mousemove", moveTooltip)
    .on("mouseleave", hideTooltip);

// Function to compute density
function kernelDensityEstimator(kernel, X) {
  return function(V) {
    return X.map(function(x) {
      return [x, d3.mean(V, function(v) { return kernel(x - v); })];
    });
  };
}
function kernelEpanechnikov(k) {
  return function(v) {
    return Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
  };
}

*/
