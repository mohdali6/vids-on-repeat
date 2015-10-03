from django.contrib import admin
from models import Video, VideoRepeats, SessionBasedRepeats
from django.contrib.sessions.models import Session


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


class VideoAdmin(admin.ModelAdmin):
    list_display = ['video_id', 'video_title']


class VideoRepeatsAdmin(admin.ModelAdmin):
    list_display = ['get_video_title', 'repeat_count']

    def get_video_title(self, obj):
        return obj.video.video_title
    get_video_title.short_description = 'Video Title'


class SessionBasedRepeatsAdmin(admin.ModelAdmin):
    list_display = ['get_session_key', 'get_video_title', 'repeat_count']

    def get_session_key(self, obj):
        return obj.session.session_key

    def get_video_title(self, obj):
        return obj.video.video_title

    get_session_key.short_description = 'Session Key'
    get_session_key.admin_order_field = 'session__session_key'

    get_video_title.short_description = 'Video Title'
    get_video_title.admin_order_field = 'video__video_title'


admin.site.register(Video, VideoAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(VideoRepeats, VideoRepeatsAdmin)
admin.site.register(SessionBasedRepeats, SessionBasedRepeatsAdmin)