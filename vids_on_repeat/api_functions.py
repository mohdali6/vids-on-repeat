from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import os
import json

## ********** Part of this code is from YouTube API samples, which are covered under Apache 2.0 License ********** ##

keyFile = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/some_data.json'

YOUTUBE_API_KEY = ""
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

with open(keyFile, 'r') as f:
    keys = json.load(f)
    if 'youtube_api_key' in keys:
        YOUTUBE_API_KEY = keys['youtube_api_key']

def youtube_search(**kwargs):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(q=kwargs['query'], part="id,snippet",
                                            maxResults=kwargs['max_results']).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
              videos.append((search_result["snippet"]["title"], search_result["id"]["videoId"]))

    return videos