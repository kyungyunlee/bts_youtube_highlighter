import os 
from apiclient.discovery import build 


playlist_ids = {
                # 'PL_Cqw69_m_yz4JcOfmZb2IDWwIuej1xfN' : 'bighit_official_movie',
                # 'PL5hrGMysD_Gt2ekpVt25B6C5ozZjVxQdh' : 'bangtantv_bts_episode',
                # 'PL5hrGMysD_GvZPFPcdm9NCqKfQKPYrkFh' : 'bangtantv_bts_festa',
                # 'PL5hrGMysD_Gu2a7-KuaQTxjRVPqM2Bi63' : 'bangtantv_bangtan_bomb',
                # 'PL5hrGMysD_GusQlLU7C06Vyklhw_HjFra' : 'bangtantv_bts_practice_video'

                # 'PL4T4Wu4qBZboYGqjpzkQ7qgQ5MeQCybx0' : 'KOOKIESTAETAS',
                # 'PL9p8yN6ZWWFgZtDeSabsaQbge20cWDscO' : 'Pinkkoyaa' ,
                # 'PLHNTFLeAcw9WFJDFYaDT_8r7JJYKEIWPg' : 'Jungkook97',
                # 'UUP1kd9bFZDVvZuCNNhuFSKw' : 'Dear_my_baby_G'
                }



def build_service(filename):
    with open(filename) as f:
        key = f.readline()

        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=key)


apikey = 'apikey.txt'
service = build_service(apikey)

# curr_playlist_id = 'UUP1kd9bFZDVvZuCNNhuFSKw'


for curr_playlist_id, playlist_name in playlist_ids.items() :  

    with open(f'../static/data/playlists/{playlist_name}.txt','w+') as playlist_f: 

        playlistitems_list_response = service.playlistItems().list(
                playlistId=curr_playlist_id, 
                part="snippet",
                maxResults=100).execute()

        while playlistitems_list_response : 
            for playlist_item in playlistitems_list_response['items']:
                title = playlist_item['snippet']['title']
                video_id = playlist_item['snippet']['resourceId']['videoId']
                print (title, video_id)
                playlist_f.write(title + '\t' + video_id + '\n') 


            if 'nextPageToken' in playlistitems_list_response:
                playlistitems_list_response = service.playlistItems().list(
                        playlistId=curr_playlist_id, 
                        part="snippet",
                        maxResults=100,
                        pageToken=playlistitems_list_response['nextPageToken']).execute()
            else :
                break 







