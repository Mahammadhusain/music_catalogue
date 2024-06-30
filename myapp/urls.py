from django.urls import path
from . import views

urlpatterns = [
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlists/create/', views.playlist_create, name='playlist_create'),
    path('playlists/<uuid:uuid>/', views.playlist_detail, name='playlist_detail'),
    path('playlists/<uuid:uuid>/update/', views.playlist_update, name='playlist_update'),
    path('playlists/<uuid:uuid>/delete/', views.playlist_delete, name='playlist_delete'),
]