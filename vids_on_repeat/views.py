from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from apiclient.errors import HttpError
from models import Video, VideoRepeats, SessionBasedRepeats
from .forms import VideoSearchForm
from .api_functions import youtube_search, video_title_search
from django.db.models import F
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.sessions.models import Session

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


@ensure_csrf_cookie
def watch_video(request, video_id):
    try:
        video_title = video_title_search(video_id)
        Video.objects.get_or_create(video_id=video_id, video_title=video_title)
    except:
        pass

    request.session['player_requested'] = True

    videoSearchForm = VideoSearchForm()
    context = {'videoId': video_id, 'videoSearchForm': videoSearchForm}

    return render(request, 'vids_on_repeat/watch.html', context)


def most_repeated_video(request):
    video_id = VideoRepeats.objects.all()[0].video_id
    return JsonResponse({'video_id': video_id})


# Function to increment overall repeats of a video by 1  #http://127.0.0.1:8000/vids/watch/ZEdUljT7eGI/
@ensure_csrf_cookie
def increment_repeat(request):
    if request.method == 'POST':
        video_id = json.loads(request.body)['video_id']
        try:
            vid, created = VideoRepeats.objects.get_or_create(video=Video.objects.get(video_id=video_id))
            vid.repeat_count = F('repeat_count') + 1
            vid.save()
        except:
            return HttpResponse(status=500)

    return HttpResponse(status=204)


@ensure_csrf_cookie
def increment_session_repeat(request):
    video_id = json.loads(request.body)['video_id']
    session_id = request.session.session_key
    request_session_key = session_id + str(video_id)

    if request.method == 'POST' and request_session_key in request.session:
        try:
            vid = SessionBasedRepeats.objects.get(pk=request.session[request_session_key])
            vid.repeat_count = F('repeat_count') + 1
            vid.save()
            return HttpResponse(status=204)
        except:
            return HttpResponse(status=500)

    elif request.method == 'POST' and request_session_key not in request.session:
        video = Video.objects.get(video_id=video_id)
        session = Session.objects.get(pk=session_id)
        try:
            vid, created = SessionBasedRepeats.objects.get_or_create(video=video, session=session)

            #Storing request_session_key in request.session dict as key and pk of vid above as value
            request.session[request_session_key] = vid.pk

            #Incrementing repeat count
            vid.repeat_count = F('repeat_count') + 1
            vid.save()
            return HttpResponse(status=204)
        except:
            return HttpResponse(status=500)

    return HttpResponse(status=405)


def session_based_repeat_count(request, video_id):
    session_video_key = request.session.session_key + str(video_id)

    if session_video_key in request.session:
        try:
            repeat_count = SessionBasedRepeats.objects.get(pk=request.session[session_video_key]).repeat_count
            return JsonResponse({'repeat_count': repeat_count})
        except:
            return HttpResponse(status=500)

    return JsonResponse({'repeat_count': 0})


#ToDo Function that returns list of top 5 trends


#ToDo
def video_durtaion(request, video_duration):
    #ToDo
    return None