from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .Views.ManagePlaylistViewSet import ArtistViewSet, AlbumViewSet, TrackViewSet, PlaylistViewSet

router = DefaultRouter()
router.register(r'artists', ArtistViewSet, basename='artists')
router.register(r'albums', AlbumViewSet, basename='albums')
router.register(r'tracks', TrackViewSet, basename='tracks')
router.register(r'playlists', PlaylistViewSet, basename='playlists')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]