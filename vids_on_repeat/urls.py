from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.video_search, name='video_search'),
    url(r'^watch/(?P<video_id>[0-9A-Za-z_-]+)/$', views.watch_video, name='watch_video'),
    url(r'^most-repeated-video/$', views.most_repeated_video, name='most_repeated_video'),
    url(r'^increment-repeat/$', views.increment_repeat, name='increment_repeat'),
]