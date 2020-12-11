import os
import json
import csv
from pathlib import Path
import random
from flask import Flask, render_template, redirect, request, jsonify, url_for
from flask_caching import Cache
from collections import defaultdict
import pickle
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import time

from data_utils import (
    join_timestamps,
    get_timestamp_list,
    create_word_frequency_table,
    get_sentiment_data,
)

###### GLOBAL VARIABLE #######
playlists = [
    "bangtantv_bangtan_bomb",
    "bangtantv_bts_episode",
    "bangtantv_bts_festa",
]  # , 'bangtantv_bts_practice_video']
all_video_fs = []
n_comments_list = []
comments_list = []
playlist_to_vid = []  # list of (playlist_name, list of videos)
all_video_comment_list = []  # list of (video_title, video_comment_file, comment_count)
all_ts_comment_list = (
    []
)  # list of (video_title, video_comment_file, timestamp, comment_count)
all_video_sentiment_list = []  # list of video sentiment data files
yt_id_to_comment_dict = {}
word_freq_list = []
wordcloud_f = "/static/wordcloud.png"


def preprocess():
    """
    Loading files before running the app
    """

    start = time.time()
    global all_video_fs, n_comments_list, comments_list
    global playlist_to_vid, all_video_comment_list, all_ts_comment_list, all_video_sentiment_list
    global yt_id_to_comment_dict
    global word_freq_list
    for playlist_name in playlists:
        playlist_video_count = 0
        lines = open(f"static/data/playlists/{playlist_name}.txt").readlines()
        lines = [line.strip("\n") for line in lines]
        lines = [line.split("\t") for line in lines]

        valid_video_titles = []

        for title, yt_id in lines:
            data_path = f"static/data/{yt_id}.csv"
            sentiment_data_path = f"static/data/sentiment/{yt_id}.csv"
            if os.path.exists(data_path):
                vid_comments = []
                comment_dict = defaultdict(list)
                with open(data_path, "r") as f:
                    reader = csv.reader(f)
                    for row in reader:
                        timestamp, comment, like_cnt = row
                        vid_comments.append(comment)
                        timestamp = int(timestamp)
                        comment_dict[timestamp].append([comment, like_cnt])

                    if data_path in all_video_fs:
                        continue

                    all_video_fs.append(data_path)
                    n_comments_list.append(len(vid_comments))
                    comments_list.extend(vid_comments)
                    valid_video_titles.append((title, yt_id))
                    all_video_comment_list.append((title, data_path, len(vid_comments)))

                    vid_comment_dict = join_timestamps(comment_dict)
                    yt_id_to_comment_dict[yt_id] = vid_comment_dict

                    for k, v in vid_comment_dict.items():
                        all_ts_comment_list.append((title, data_path, k, len(v)))

                    playlist_video_count += 1

            if os.path.exists(sentiment_data_path):
                all_video_sentiment_list.append(sentiment_data_path)

        playlist_to_vid.append((playlist_name, valid_video_titles))
        print(f"Number of videos for {playlist_name} :", playlist_video_count)

    # Load word frequency list
    word_freq_f = "static/word_freq.pkl"
    if not os.path.exists(word_freq_f):
        print("Computing word frequency")
        word_freq_list = create_word_frequency_table(comments_list)
        pickle.dump(word_freq_list, open(word_freq_f, "wb"))
        # Make wordcloud
        print("Making wordcloud")
        keyword_dict = {}
        for keyword in word_freq_list:
            keyword_dict[keyword[0]] = keyword[1]

        top = cm.get_cmap("Purples", 128)
        bottom = cm.get_cmap("Blues", 128)

        newcolors = np.vstack(
            (top(np.linspace(0.5, 1, 200)), bottom(np.linspace(0.5, 1, 56)))
        )
        newcmp = ListedColormap(newcolors, name="OrangeBlue")

        wordcloud = WordCloud(
            width=800,
            height=800,
            background_color="rgba(255,255,255,0)",
            mode="RGBA",
            colormap=newcmp,
            min_font_size=10,
            max_words=10000,
            font_path="static/Montserrat-Regular.otf",
            repeat=False,
        ).generate_from_frequencies(keyword_dict)

        wordcloud.to_file(wordcloud_f)

    else:
        print("already computed")
        word_freq_list = pickle.load(open(word_freq_f, "rb"))

    print("preprocessing time", time.time() - start)


preprocess()
app = Flask(__name__)
cache = Cache(app, config={"CACHE_TYPE": "simple"})


@app.route("/")
def index():
    # return render_template("index.html")
    return redirect(url_for('overview'))


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/main")
def overview():
    n_videos = len(all_video_fs)
    avg_comments = round(sum(n_comments_list) / len(n_comments_list), 1)

    return render_template(
        "overview.html",
        n_videos=n_videos,
        n_comments=sum(n_comments_list),
        avg_comments=avg_comments,
    )


@app.route("/main/moments/<idx>")
def notable_moments(idx):

    ########  Most commented scenes #########
    # Per clip, get a thumbnail gif, title, display keywords, number of comments, sample comments
    sorted_comment = sorted(all_ts_comment_list, key=lambda x: x[3], reverse=True)
    print(len(sorted_comment))
    most_commented_scenes = []
    for vid in sorted_comment[int(idx) * 10 : 10 * (int(idx) + 1)]:
        curr_title = vid[0]
        curr_yt_id = Path(vid[1]).stem
        curr_timestamp = vid[2]
        curr_n_comments = vid[3]
        curr_comments = yt_id_to_comment_dict[curr_yt_id][curr_timestamp]
        # subtract 3 seconds for the video start time
        curr_timestamp = str(int(curr_timestamp) - 3)
        # convert to min:ss
        m = int(curr_timestamp) // 60
        s = int(curr_timestamp) - (60 * m)
        curr_timestamp_str = "%02d:%02d" % (m, s)
        most_commented_scenes.append(
            (
                curr_title,
                curr_yt_id,
                curr_timestamp,
                curr_timestamp_str,
                curr_n_comments,
                curr_comments,
            )
        )

    return render_template(
        "popular_videos.html", most_commented_scenes=most_commented_scenes
    )


@app.route("/main/keywords")
def overall_keywords():
    global word_freq_list
    # Top N keywords
    keywords = word_freq_list[:50]
    return render_template("keywords.html", keywords=keywords, wordcloud_f=wordcloud_f)


@app.route("/main/sentiment")
def overall_sentiment():

    # Sentiment analysis
    sentiment_score_list, score_to_comment_dict_ = get_sentiment_data(
        all_video_sentiment_list
    )

    score_to_comment_dict = {}
    for k, v in score_to_comment_dict_.items():
        # random.shuffle(v)
        score_to_comment_dict[k] = v[:100]
    score_to_comment_dict_ = {}
    # sentiment_score_list = []
    # score_to_comment_dict = {"asdfa" :"asdfsdf"}
    return render_template(
        "sentiment.html",
        sentiment_score_list=sentiment_score_list,
        sentiment_score_dict=score_to_comment_dict,
    )


@app.route("/analysis")
@cache.cached(timeout=50)
def general_analysis():
    global word_freq_list

    n_videos = len(all_video_fs)
    avg_comments = round(sum(n_comments_list) / len(n_comments_list), 1)

    #######  Most commented video ########
    """
    # Per video, thumbnail, number of comment counts
    sorted_vid = sorted(all_video_comment_list, key=lambda x: x[2], reverse=True)

    most_commented_videos = []
    for vid in sorted_vid[:10]:
        most_commented_videos.append((vid[0], Path(vid[1]).stem, vid[2]))
    """

    ########  Most commented scenes #########
    # Per clip, get a thumbnail gif, title, display keywords, number of comments, sample comments
    sorted_comment = sorted(all_ts_comment_list, key=lambda x: x[3], reverse=True)
    print(len(sorted_comment))
    most_commented_scenes = []
    for vid in sorted_comment[:30]:
        curr_title = vid[0]
        curr_yt_id = Path(vid[1]).stem
        curr_timestamp = vid[2]
        curr_n_comments = vid[3]
        curr_comments = yt_id_to_comment_dict[curr_yt_id][curr_timestamp]
        # subtract 3 seconds for the video start time
        curr_timestamp = str(int(curr_timestamp) - 3)
        # convert to min:ss
        m = int(curr_timestamp) // 60
        s = int(curr_timestamp) - (60 * m)
        curr_timestamp_str = "%02d:%02d" % (m, s)
        most_commented_scenes.append(
            (
                curr_title,
                curr_yt_id,
                curr_timestamp,
                curr_timestamp_str,
                curr_n_comments,
                curr_comments,
            )
        )

    # Top N keywords
    keywords = word_freq_list[:50]

    # Sentiment analysis
    start = time.time()
    sentiment_score_list, score_to_comment_dict_ = get_sentiment_data(
        all_video_sentiment_list
    )

    score_to_comment_dict = {}
    for k, v in score_to_comment_dict_.items():
        # random.shuffle(v)
        score_to_comment_dict[k] = v[:100]
    score_to_comment_dict_ = {}
    # sentiment_score_list = []
    # score_to_comment_dict = {"asdfa" :"asdfsdf"}
    print("sentiment data time", time.time() - start)

    return render_template(
        "analysis.html",
        n_videos=n_videos,
        n_comments=sum(n_comments_list),
        avg_comments=avg_comments,
        # most_commented_videos=most_commented_videos,
        most_commented_scenes=most_commented_scenes,
        keywords=keywords,
        wordcloud_f=wordcloud_f,
        sentiment_score_list=sentiment_score_list,
        sentiment_score_dict=score_to_comment_dict,
    )


@app.route("/video")
def video_index_page():
    return render_template("video_main.html", playlist_list=playlist_to_vid)


@app.route("/video/<youtube_id>", methods=["GET", "POST"])
def show_video_data(youtube_id):
    curr_comment = yt_id_to_comment_dict[youtube_id]
    timestamp_list = get_timestamp_list(curr_comment)
    n_comments = len(timestamp_list)
    
    '''
    timestamp_comment = ""
    if request.method == 'POST': 
        jsdata = request.form['javascript_data']
        if jsdata in curr_comment.keys():
            timestamp_comment = curr_comment[jsdata]
    '''
    comment_list = []
    for k, v in curr_comment.items():
        for v_ in v:
            comment_list.append(v_[0])

    keywords = create_word_frequency_table(comment_list)
    keywords = keywords[:10]
    sentiment_f = f"static/data/sentiment/{youtube_id}.csv"
    sentiments = []
    if os.path.exists(sentiment_f):
        with open(sentiment_f, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                _, _, _, sentiment_score = row
                sentiments.append(round(float(sentiment_score), 1))
    
    
    return render_template(
        "video.html",
        playlist_list=playlist_to_vid,
        youtube_id=youtube_id,
        comments=curr_comment,
        counts=timestamp_list,
        n_comments=n_comments,
        keywords=keywords,
        sentiments=sentiments,
        # timestamp_comment=timestamp_comment
    )


if __name__ == "__main__":
    # app.jinja_env.cache = {}

    app.run(debug=True, use_reloader=True)
