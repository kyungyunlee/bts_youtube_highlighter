
// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player_elem = document.getElementById("player");
console.log(player_elem.textContent);
var comment_dict = document.getElementById("comments").textContent;
// comment_dict = comment_dict.replace(/'/g,"\"");
comment_dict = JSON.parse(comment_dict);


var start = 0;
var interval = 1000;
var interval_function; 

var vid_width = window.innerWidth * 0.5; //'640';
var vid_height = vid_width * 390/640;

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: vid_height,
    width: vid_width,
    videoId: player_elem.textContent,
    playerVars : {'origin':'https://localhost:5000'},
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

function onPlayerReady(event) {
//   event.target.playVideo();
    console.log(player.getCurrentTime());
    // setInterval(doAjax, interval);
    console.log(player.getDuration());
    plot_hist(player.getDuration());

}

function onPlayerStateChange(event) {
    // fetch('/video/'+player_elem.textContet).then(function(response){
    //     return response.json();
    // }) 
    var currentTime = player.getCurrentTime();
    currentTime = Math.round(currentTime).toString();

    $.ajax({
        type: "POST",
        contentType: "application/json;charset=utf-8",
        url: "/video/" + player_elem.textContent,
        traditional: "true",
        data: JSON.stringify({currentTime}),
        // dataType: "json",
        success : function(response){
            
            if (comment_dict[currentTime] !== undefined){ 
                $('#comments').text(comment_dict[currentTime]);
            } 
        },
        });

    if (player.getPlayerState() == 1){
        console.log("playing");
        interval_function = setInterval(doAjax, interval);
    } else {
        clearTimeout(interval_function);
    }

}



function doAjax() {

    console.log("ajax");
    var currentTime = player.getCurrentTime();
    currentTime = Math.round(currentTime).toString();
    $.ajax({
            type: 'POST',
            url: "/video/" + player_elem.textContent,
            contentType: "application/json;charset=utf-8",
            // data: $(this).serialize(),
            data: JSON.stringify({currentTime}),
            // dataType: 'json',
            traditional: "true",
            success: function (data) {
                if (comment_dict[currentTime] !== undefined){ 
                    $('#comments').text(comment_dict[currentTime]);
                } 
            },

    });

}


function plot_hist(duration) { 
    var data = document.getElementById("counts").textContent;
    data_list_ = JSON.parse(data);
    
    var data_list = [];
    for (var i = 0, len = data_list_.length; i < len; i++) {
        if (data_list_[i] <= duration) { 
            data_list.push(data_list_[i]);
        }
    }

    // console.log("!!!!!");

    var domain = [0, duration ]; 
    var margin = { top: 30, right: 0, bottom: 30, left:0 },

    width = window.innerWidth *0.7 - margin.left - margin.right,
    height = window.innerHeight*0.5 - margin.top - margin.bottom;
    
    // The number of bins 
    var Nbin = duration;

    /*
    console.log(Nbin);
    var new_Nbin = Nbin;
    while (new_Nbin > 500) {
      new_Nbin /= 2;
    }
    new_Nbin = Math.round(new_Nbin);
    // regroup comment_dict if the video duration is too long 
    if (new_Nbin != Nbin) {
      new_comment_dict = {} 
      var step = Math.round(Nbin / new_Nbin);
      console.log(step);
      var key_list = Object.keys(comment_dict);
      for (var i=0; i < new_Nbin; i++) {
        new_comment_dict[i*step] = []
        for (var k=i * step; k < (i+1)*step; k++){
          if (key_list.includes(k.toString())) {
            new_comment_dict[i*step].push(...comment_dict[k.toString()]);
          }
        }
      }
      Nbin = new_Nbin;
    } else { 
      new_comment_dict = comment_dict;
    } 
    */

    new_comment_dict = comment_dict;


    console.log(new_comment_dict);
    console.log(comment_dict);


    var x = d3
    .scaleLinear()
    .domain(domain) 
    .range([0, width]);


    // Histogram 
    var histogram = d3
    .histogram()
    .domain(x.domain()) // then the domain of the graphic
    .thresholds(x.ticks(Nbin)); // then the numbers of bins
    
    // And apply this function to data to get the bins
    var bins = histogram(data_list);





    var svg = d3
    .select("#dist_graph")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg
    .append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x))
    .attr("align", "center");

    var y = d3
    .scaleLinear()
    .range([height, 0])
    .domain([
        0,
        d3.max(bins, function(d) {
        return d.length;
        })
    ]); 
    
    svg.append("g").call(d3.axisLeft(y));

    /// ADD TOOL TIP 
    var tooltip = d3.select("#dist_graph")
    .append("div")
    .style("opacity", 0)
    .attr("class", "tooltip")
    .style("background-color", "black")
    .style("color", "white")
    .style("border-radius", "5px")
    .style("padding", "10px")

  // A function that change this tooltip when the user hover a point.
  // Its opacity is set to 1: we can now see it. Plus it set the text and position of tooltip depending on the datapoint (d)
  var showTooltip = function(d, i) {
    tooltip
      .transition()
      .duration(100)
      .style("opacity", 1)
    tooltip
      // .html("Range: " + i.x0 + " - " + i.x1)
      .html(new_comment_dict[i.x0])
      .style("left", (d3.mouse(this)[0]+20) + "px")
      .style("top", (d3.mouse(this)[1]) + "px")
  }
  var moveTooltip = function(d, i) {
    tooltip
    .style("left", (d3.mouse(this)[0]+20) + "px")
    .style("top", (d3.mouse(this)[1]) + "px")
  }
  // A function that change this tooltip when the leaves a point: just need to set opacity to 0 again
  var hideTooltip = function(d) {
    tooltip
      .transition()
      .duration(100)
      .style("opacity", 0)
  }


  var move_playback_position = function(d, i){
      player.seekTo(i.x0);
  }

    svg
    .selectAll("rect")
    .data(bins)
    .enter()
    .append("rect")
    .attr("x", 1)
    .attr("transform", function(d) {
        return "translate(" + x(d.x0) + "," + y(d.length) + ")";
    })
    .attr("width", function(d) {
        return x(d.x1) - x(d.x0) - 1;
    })
    .attr("height", function(d) {
        return height - y(d.length);
    })
    .style("fill", "#9400D3")
    // Show tooltip on hover
    .on("mouseover", showTooltip )
    .on("mousemove", moveTooltip )
    .on("mouseleave", hideTooltip )
    .on("click", move_playback_position )


}


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
