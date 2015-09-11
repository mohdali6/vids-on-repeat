from django.shortcuts import render, redirect
from django.http import HttpResponse
from apiclient.errors import HttpError

from .forms import VideoSearchForm
from .api_functions import youtube_search

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
    print video_id
    #ToDo get video player

    return render(request, 'vids_on_repeat/watch.html', {'form':VideoSearchForm})