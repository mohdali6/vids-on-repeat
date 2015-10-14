from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import os
import json
import requests

## ********** Part of this code is from YouTube API samples, which are covered under Apache 2.0 License ********** ##

keyFile = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/some_data.json'

YOUTUBE_API_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# OpenAura API

OPEN_AURA_KEY = ""
OPEN_AURA_ARTIST_SEARCH = "http://api.openaura.com/v1/search/artists?"


with open(keyFile, 'r') as f:
    keys = json.load(f)
    if 'youtube_api_key' in keys:
        YOUTUBE_API_KEY = keys['youtube_api_key']
    OPEN_AURA_KEY = str(keys.get('open_aura_key'))


def youtube_search(**kwargs):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(q=kwargs['query'], part="id,snippet",
                                            maxResults=kwargs['max_results']).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
              videos.append((search_result["snippet"]["title"], search_result["id"]["videoId"]))

    return videos


def video_title_search(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
    video_response = youtube.videos().list(id=video_id,
                                           part='snippet').execute()
    return video_response["items"][0]["snippet"]["title"]


# Searches Open Aura taking artist name as query parameter
def open_aura_search(query):
    open_aura_artist_search_url = OPEN_AURA_ARTIST_SEARCH + "q=" + query + "&api_key=" + OPEN_AURA_KEY
    r = requests.get(open_aura_artist_search_url)
    return r.json()