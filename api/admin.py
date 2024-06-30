from django.contrib import admin
from .models import Artist, Album, Track, Playlist, PlaylistTrack

class PlaylistTrackInline(admin.TabularInline):
    model = PlaylistTrack
    extra = 1

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'uuid')
    inlines = [PlaylistTrackInline]

admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(Track)