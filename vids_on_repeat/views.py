from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import VideoSearchForm
from .api_functions import youtube_search

MAX_RESULTS = '15'

def index(request):
    form = VideoSearchForm()
    return render(request, 'vids_on_repeat/index.html', {'form': form})

def video_search(request):
    if 'search_query' in request.GET and request.GET['search_query']:
        videoList = youtube_search(query=request.GET['search_query'], max_results=MAX_RESULTS)
        print videoList
        return HttpResponse("Display search results")
    else:
        return redirect('/vids/')