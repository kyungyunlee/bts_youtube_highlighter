import os 
import csv 
from flask import Flask, render_template, request, jsonify, url_for 
from collections import defaultdict 
from data_utils import join_timestamps, get_timestamp_list  

###### GLOBAL VARIABLE #######
playlists = ['bangtantv_bangtan_bomb', 'bangtantv_bts_episode', 'bangtantv_bts_festa']
all_video_fs = [] 
playlist_to_vid = [] # list of (playlist_name, list of videos)
all_video_comment_list = [] # list of (video_title, video_comment_file, comment_count)
all_ts_comment_list = [] # list of (video_title, video_comment_file, timestamp, comment_count)
all_video_sentiment_list = [] # list of video sentiment data files 
yt_id_to_comment_dict = {} 


def preprocess () : 
    for playlist_name in playlists :
        playlist_video_count = 0 
        lines = open(f'static/data/playlists/{playlist_name}.txt').readlines()
        lines = [line.strip('\n') for line in lines]
        lines = [line.split('\t') for line in lines]
        
        valid_video_titles = [] 
        
        for title, yt_id in lines : 
            data_path = f'static/data/{yt_id}.csv'
            if os.path.exists(data_path):
                vid_comments = [] 
                comment_dict = defaultdict(list) 
                with open(data_path, 'r') as f: 
                    reader = csv.reader(f) 
                    for row in reader : 
                        timestamp, comment, like_cnt = row 
                        vid_comments.append(comment)
                        timestamp = int(timestamp)
                        comment_dict[timestamp].append([comment, like_cnt])

                    if data_path in all_video_fs : 
                        continue 

                    all_video_fs.append((playlist_name, data_path))
                    valid_video_titles.append((title, yt_id))
                    all_video_comment_list.append((title, data_path, len(vid_comments)))
                    
                    vid_comment_dict = join_timestamps(comment_dict)
                    yt_id_to_comment_dict[yt_id] = vid_comment_dict 

                    for k,v in vid_comment_dict.items():
                        all_ts_comment_list.append((title, data_path, k, len(v)))

                    playlist_video_count +=1 
        
        playlist_to_vid.append((playlist_name, valid_video_titles))
        print (f"Number of videos for {playlist_name} :", playlist_video_count)


preprocess() 
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about_page():
    return render_template('about.html') 

@app.route('/analysis')
def general_analysis():
    #######  Most commented video ########
    # Per video, thumbnail, number of comment counts 
    sorted_vid = sorted(all_video_comment_list, key=lambda x:x[2], reverse=True)
    for vid in sorted_vid[:10]:
        print (vid[0], vid[1], len(vid[2])) 

    ########  Most commented scenes #########
    # Per clip, get a thumbnail gif, title, display keywords, number of comments, sample comments  
    sorted_comment = sorted(all_ts_comment_list, key=lambda x: x[3], reverse=True)

    for vid in sorted_comment[:10]:
        print (vid[0], vid[1], vid[2], len(vid[3]))

    # Top keywords 

    # Sentiment analysis 

    return 

@app.route('/video')
def video_index_page():
    return render_template('video_main.html', playlist_list=playlist_to_vid) 


@app.route('/video/<youtube_id>', methods=['GET', 'POST'])
def show_video_data(youtube_id):
    comment_dict = yt_id_to_comment_dict[youtube_id]
    timestamp_list = get_timestamp_list(comment_dict)

    return render_template('video.html', playlist_list=playlist_to_vid, youtube_id=youtube_id, comments=comment_dict, counts=timestamp_list) 

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
