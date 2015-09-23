from django.contrib import admin
from models import Video, VideoRepeats
from django.contrib.sessions.models import Session


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

admin.site.register(Video)
admin.site.register(Session, SessionAdmin)
admin.site.register(VideoRepeats)