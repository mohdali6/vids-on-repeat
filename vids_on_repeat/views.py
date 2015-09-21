from django.shortcuts import render, redirect
from django.http import HttpResponse
from apiclient.errors import HttpError
from models import Video

from .forms import VideoSearchForm
from .api_functions import youtube_search, video_title_search

MAX_RESULTS = '15'
WATCH_URL = '/vids/watch/'


def index(request):
    form = VideoSearchForm()
    context = {'form': form}

    if 'error' in request.session.keys() and request.session['error'] == True:
        request.session['error'] = False
        context = {'form': form, 'error': True}

    return render(request, 'vids_on_repeat/index.html', context)


def video_search(request):
    if 'search_query' in request.GET and request.GET['search_query']:
        try:
            videoList = youtube_search(query=request.GET['search_query'], max_results=MAX_RESULTS)
            return render(request, 'vids_on_repeat/result.html', {'videoList': videoList, 'form': VideoSearchForm})
        except HttpError, e:
            print "An HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
            request.session['error'] = True
            return redirect('/vids/')
    else:
        return redirect('/vids/')


def watch_video(request, video_id):
    try:
        video_title = video_title_search(video_id)
        Video.objects.get_or_create(video_id=video_id, video_title=video_title)
    except:
        pass

    videoSearchForm = VideoSearchForm()
    context = {'videoId': video_id, 'videoSearchForm':videoSearchForm}

    return render(request, 'vids_on_repeat/watch.html', context)

#ToDo Function that returns most repeated video_id

#ToDo Function that returns list of top 5 trends

def video_durtaion(request, video_duration):
    #ToDo
    return None