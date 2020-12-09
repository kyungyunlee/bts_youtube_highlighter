var score_list_data = document.getElementById("sentiment_score_list")
  .textContent;
score_list_data = JSON.parse(score_list_data);
score_list_data = score_list_data.map(Number);
var score_dict = document.getElementById("sentiment_score_dict").textContent;
score_dict = JSON.parse(score_dict);

var new_score_dict = {};

Object.entries(score_dict).forEach(([k, v]) => {
  new_score_dict[parseFloat(k)] = v;
});
score_dict = {};
var comment_list = [];
for (var i = -1.0; i <= 1.0; i += 0.1) {
  if (i.toFixed(1) == 0.0) {
    comment_list.push(new_score_dict[0]);
  } else if (i.toFixed(1) == -1.0) {
    comment_list.push(new_score_dict[-1.0]);
  } else if (i.toFixed(1) == 1.0) {
    comment_list.push(new_score_dict[1.0]);
  } else {
    comment_list.push(new_score_dict[i.toFixed(1)]);
  }
}

var myPlot = document.getElementById("sentiment_viz");
var hoverInfo = document.getElementById("sentiment-comment-content");
var d3 = Plotly.d3;

var trace = {
  x: score_list_data,
  type: "histogram",
  autobinx: false,
  text: comment_list,
  xbins: {
    end: 1.0,
    start: -1.0,
    size: 0.1,
  },
  marker: {
    cmax: 20,
    cmin: 0,
    color: [...Array(20).keys()].reverse(),
    colorscale: "RdBu",
  },
};

var data = [trace];
var layout = {
  paper_bgcolor: "rgba(255,255,255,0)",
  plot_bgcolor: "rgba(255,255,255,0)",
  xaxis: {
    domain: [-1, 1],
    title: "Sentiment score",
    rangemode: "tozero",
  },
  yaxis: {
    title: "Counts",
  },
};
var config = { responsive: true };
Plotly.newPlot("sentiment_viz", data, layout, config);

myPlot.on("plotly_click", function (data) {
  var bin_num = data.points[0].binNumber;
  hoverInfo.innerHTML = data.points[0].data.text[bin_num];
});
