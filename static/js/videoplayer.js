// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement("script");

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName("script")[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

var player_elem = document.getElementById("player");
console.log(player_elem.textContent);
var comment_dict = document.getElementById("all-comments").textContent;
// comment_dict = comment_dict.replace(/'/g,"\"");
comment_dict = JSON.parse(comment_dict);

var start = 0;
var interval = 1000;
var interval_function;

var vid_width = "100%"; // window.innerWidth * 0.4; //'640';
var vid_height = "auto"; // vid_width * 390/640;

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player("player", {
    height: vid_height,
    width: vid_width,
    videoId: player_elem.textContent,
    playerVars: { origin: "http://www.youtube.come" },
    //https://localhost:5000" },
    events: {
      onReady: onPlayerReady,
      onStateChange: onPlayerStateChange,
    },
  });
}

function onPlayerReady(event) {
  //   event.target.playVideo();
  console.log(player.getCurrentTime());
  // setInterval(doAjax, interval);
  console.log(player.getDuration());
  plot_hist(player.getDuration());
  plot_sentiment();
}

function onPlayerStateChange(event) {
  // fetch('/video/'+player_elem.textContet).then(function(response){
  //     return response.json();
  // })
  var currentTime = player.getCurrentTime();
  currentTime = Math.round(currentTime).toString();
  
  /* 
  $.ajax({
    type: "POST",
    contentType: "application/json;charset=utf-8",
    url: "/video/" + player_elem.textContent,
    traditional: "true",
    data: JSON.stringify({ currentTime }),
    // dataType: "json",
    success: function (response) {
      console.log("change");
      if (comment_dict[currentTime] !== undefined) {
        $("#timestamp_comments").text(comment_dict[currentTime]);
      }
    },
  });
  */
  $("#timestamp_comments").text(comment_dict[currentTime]);
  
  /*
  $.post("/video/" + player_elem.textContent,  {
     javascript_data: currentTime
  });
  */

  if (player.getPlayerState() == 1) {
    console.log("playing");
    interval_function = setInterval(doAjax, interval);
  } 
   else {
     console.log("stop")
    clearTimeout(interval_function);
   }
}

function doAjax() {
  var currentTime = player.getCurrentTime();
  currentTime = Math.round(currentTime).toString();
  /*
  $.ajax({
    type: "POST",
    url: "/video/" + player_elem.textContent,
    contentType: "application/json;charset=utf-8",
    // data: $(this).serialize(),
    data: JSON.stringify({ currentTime }),
    // dataType: 'json',
    traditional: "true",
    success: function (data) {
      console.log("ajaxadfasdf")
      if (comment_dict[currentTime] !== undefined) {
        $("#timestamp_comments").text(comment_dict[currentTime]);
      }
    },
  });
  */
  $("#timestamp_comments").text(comment_dict[currentTime]);

  /*
  $.post("/video/" + player_elem.textContent,  {
     javascript_data: currentTime
  });
  */
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
  var comment_list = [];
  for (var i = 0; i < duration; i++) {
    if (comment_dict.hasOwnProperty(i)) {
      comment_list.push(comment_dict[i].toString());
    } else {
      if (comment_list.length > 0) {
        comment_list.push(i);
      }
    }
  }
  var myPlot = document.getElementById("comment_graph"),
    hoverInfo = document.getElementById("hoverInfo"),
    d3 = Plotly.d3,
    data = [
      {
        x: data_list,
        type: "histogram",
        nbinx: duration + 1,
        xbins: { end: duration, start: -0.5, size: 1 },
        text: comment_list,
        hovertemplate: "%{text}" + "<extra></extra>",
        marker: {
          color: "rgba(128, 0, 128, 0.7)",
        },
      },
    ],
    layout = {
      hovermode: "closest",
      xaxis: {
        showline: true,
        domain: [0, duration],
        title: "time(s)",
        showgrid: true,
        rangemode: "tozero",
      },
      yaxis: {
        title: "Counts",
      },
      hoverlabel: { bgcolor: "white" },
      paper_bgcolor: "rgba(255,255,255,0)",
      plot_bgcolor: "rgba(255,255,255,0)",
    };

  var config = { responsive: true };

  Plotly.newPlot("comment_graph", data, layout, config);

  myPlot.on("plotly_click", function (data) {
    player.seekTo(data.points[0].x);
  });
}

function plot_sentiment() {
  // Sentiment histogram
  var sentiment_data = document.getElementById("video_sentiments").textContent;
  sentiment_data = JSON.parse(sentiment_data);
  sentiment_data = sentiment_data.map(Number);

  // sentiment_data = [0, 0.2, 0.4, 0.2, 0.2 , 0.2, -0.1]
  var trace = {
    x: sentiment_data,
    type: "histogram",
    autobinx: false,
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
      showline: true,
      domain: [-1, 1],
      title: "Sentiment score",
      showgrid: true,
      rangemode: "tozero",
    },
    yaxis: {
      title: "Counts",
    },
  };
  var config = { responsive: true };

  Plotly.newPlot("sentiment_graph", data, layout, config);
}
