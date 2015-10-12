from django.conf.urls import url

from . import views

urlpatterns = [  # increment-session-repeat
                 url(r'^$', views.index, name='index'),
                 url(r'^search/$', views.video_search, name='video_search'),
                 url(r'^watch/(?P<video_id>[0-9A-Za-z_-]+)/$', views.watch_video, name='watch_video'),
                 url(r'^most-repeated-videos/$', views.most_repeated_videos, name='most_repeated_videos'),
                 url(r'^increment-repeat/$', views.increment_repeat, name='increment_repeat'),
                 url(r'^increment-session-repeat/$', views.increment_session_repeat, name='increment_session_repeat'),
                 url(r'get-total-views/(?P<video_id>[0-9A-Za-z_-]+)/$', views.total_views, name='total_views'),
                 url(r'^get-session-based-repeat-count/(?P<video_id>[0-9A-Za-z_-]+)/$', views.session_based_repeat_count, name='session_based_repeat_count'),
                 ]