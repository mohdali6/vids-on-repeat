from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import VideoSearchForm

def index(request):
    form = VideoSearchForm()
    return render(request, 'vids_on_repeat/index.html', {'form': form})

def video_search(request):
    if 'search_query' in request.GET and request.GET['search_query']:
        return HttpResponse("Display search results")
    else:
        return redirect('/vids/')