import os 
from multiprocessing import Pool
import csv 
from collections import defaultdict 
from apiclient.discovery import build

def build_service(filename):
    with open(filename) as f:
        key = f.readline()

        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=key)

apikey = 'apikey.txt'
service = build_service(apikey)
print ("youtube api connected")


def download_youtube_comments(youtube_id, comment_f):
    """
    Download and save youtube comments to csv file 
    """
    timepattern = "(?:([0-5]?[0-9]):)?([0-5]?[0-9]):([0-5][0-9])"
    
    try : 
        response = service.commentThreads().list(
                part='snippet',
                maxResults=100,
                textFormat='plainText',
                order='time',
                videoId=youtube_id
                ).execute()
    except : 
        print ("Invalid youtube id")
        return None 
    
    comment_dict = defaultdict(list)

    page = 0

    with open(comment_f,'w+') as f:
        while response:
            print("page",youtube_id, page)
            page += 1 
            index = 0
            for item in response['items']:
                # print(f"comment {index}")
                index +=1 
                
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
                
                z = re.match(timepattern, comment)
                if z : 
                    str_t = z.group(0) 
                    str_min = int(str_t.split(':')[0])
                    str_sec = int(str_t.split(':')[1])
                    time = str_min * 60 + str_sec 
                    comment_dict[time].append( [comment, like_count])

                    csvwriter = csv.writer(f)
                    csvwriter.writerow([time, comment, like_count])
                
                
            if 'nextPageToken' in response:
                response = service.commentThreads().list(
                            part='snippet',
                            maxResults=100,
                            textFormat='plainText',
                            order='time',
                            videoId=youtube_id,
                            pageToken=response['nextPageToken'] 
                        ).execute()
            else :
                break 

    return comment_dict


def run_process(yt_id) :
    comment_f = os.path.join("static/data", yt_id + '.csv')
    if os.path.exists(comment_f): 
        print ("already done")
    else : 
        comments = download_youtube_comments(yt_id, comment_f)
    print (yt_id)



if __name__ == '__main__':
    # Analyse all data 
    playlist_names =  ['bighit_official_movie'] # ['bangtantv_bangtan_bomb'] #  ['bighit_official_movie']# 'Jungkook97'] # 'Pinkkoyaa'] #'Dear_my_baby_G'] # 'bangtantv_bts_episode'] # 'KOOKIESTAETAS'] # 'bangtantv_bts_festa']

    all_videos = [] 
    for playlist_name in playlist_names : 
        f = open (os.path.join('static/data/playlists', playlist_name + '.txt'))
        all_videos.extend(f.readlines())

    all_videos = [vid.strip('\n').split('\t')[1] for vid in all_videos]
    print (len(all_videos))
    for vid in all_videos : 
        run_process(vid) 

    # with Pool(2) as p :
    #    p.map(run_process, all_videos)
    
    '''
    error_files = [] 
    for vid in all_videos : 
        out = check_download(vid)
        if out :
            error_files.append(out)
    print (len(error_files))
    error_files = all_videos 
    for error_file in error_files :
        run_process(error_file) 
    '''
