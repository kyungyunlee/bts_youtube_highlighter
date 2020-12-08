import os
import csv
from pathlib import Path
import requests
from langdetect import detect
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def sentiment_analysis(playlists):
    """
    Perform sentiment analysis.
    Do this and save it in another file.
    """

    languages = [
        "English",
        "French",
        "German",
        "Spanish",
        "Italian",
        "Russian",
        "Japanese",
        "Arabic",
        "Chinese(Simplified)",
        "Chinese(Traditional)",
    ]
    language_codes = ["en", "fr", "de", "es", "it", "ru", "ja", "ar", "zh-CN", "zh-TW"]
    sentences = []

    all_files = []
    # playlists = ["bangtantv_bangtan_bomb"] # "bangtantv_bts_festa"]
    for playlist_name in playlists:
        lines = open(
            os.path.join("../static/data/playlists", playlist_name + ".txt")
        ).readlines()
        lines = [line.strip("\n") for line in lines]
        lines = [line.split("\t")[1] for line in lines]
        for line in lines:
            video_path = f"../static/data/{ line }.csv"
            if os.path.exists(video_path):
                all_files.append(video_path)
    print(len(all_files))
    save_dir = "../static/data/sentiment/"

    analyzer = SentimentIntensityAnalyzer()

    for curr_f in all_files:
        save_f = os.path.join(save_dir, Path(curr_f).stem + ".csv")
        if os.path.exists(save_f):
            print("already done")
            continue

        with open(save_f, "w") as write_f:
            writer = csv.writer(write_f)
            with open(curr_f) as f:
                reader = csv.reader(f)
                for row in reader:
                    timestamp, sentence, like_cnt = row

                    to_lang = "en"
                    try:
                        from_lang = detect(sentence)
                    except:
                        print("cannot detect language", sentence)
                        continue

                    if (from_lang == "en") or (from_lang == "en-US"):
                        translation = sentence
                        translator_name = "No translation needed"
                    else:
                        api_url = "http://mymemory.translated.net/api/get?q={}&langpair={}|{}".format(
                            sentence, from_lang, to_lang
                        )
                        hdrs = {
                            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
                            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                            "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
                            "Accept-Encoding": "none",
                            "Accept-Language": "en-US,en;q=0.8",
                            "Connection": "keep-alive",
                        }
                        response = requests.get(api_url, headers=hdrs)
                        try:
                            response_json = json.loads(response.text)
                        except:
                            continue
                        translation = response_json["responseData"]["translatedText"]
                        translator_name = "MemoryNet Translation Service"

                    if translation:
                        vs = analyzer.polarity_scores(translation)
                        print(
                            "- {: <8}: {: <69}\t {} ({})".format(
                                from_lang,
                                sentence,
                                str(vs["compound"]),
                                translator_name,
                            )
                        )
                        writer.writerow(
                            [timestamp, sentence, like_cnt, str(vs["compound"])]
                        )


if __name__ == "__main__":
    playlists = [
        "bangtantv_bangtan_bomb",
        "bangtantv_bts_festa",
        "bangtantv_bts_episode",
    ]
    sentiment_analysis(playlists)
