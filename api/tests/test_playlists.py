from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from api.models import Playlist, Track, Artist, Album
import uuid

class PlaylistTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.artist = Artist.objects.create(name="Test Artist")
        self.album = Album.objects.create(title="Test Album", artist=self.artist)
        self.track1 = Track.objects.create(title="Test Track 1", album=self.album)
        self.track2 = Track.objects.create(title="Test Track 2", album=self.album)

    def test_create_playlist(self):
        url = reverse('playlists-list')
        data = {
            "name": "Test Playlist",
            "tracks": [
                {"track": self.track1.id, "order": 1},
                {"track": self.track2.id, "order": 2}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Playlist.objects.count(), 1)
        playlist = Playlist.objects.first()
        self.assertEqual(playlist.name, "Test Playlist")
        self.assertEqual(playlist.tracks.count(), 2)

    def test_get_playlist_list(self):
        Playlist.objects.create(name="Test Playlist 1")
        Playlist.objects.create(name="Test Playlist 2")
        url = reverse('playlists-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_playlist_detail(self):
        playlist = Playlist.objects.create(name="Test Playlist")
        url = reverse('playlists-detail', kwargs={'uuid': playlist.uuid})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test Playlist")

    def test_update_playlist(self):
        playlist = Playlist.objects.create(name="Test Playlist")
        url = reverse('playlists-detail', kwargs={'uuid': playlist.uuid})
        data = {
            "name": "Updated Playlist",
            "tracks": [
                {"track": self.track1.id, "order": 1}
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Playlist.objects.get(uuid=playlist.uuid).name, "Updated Playlist")

    def test_delete_playlist(self):
        playlist = Playlist.objects.create(name="Test Playlist")
        url = reverse('playlists-detail', kwargs={'uuid': playlist.uuid})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Playlist.objects.count(), 0)

    def test_add_track_to_playlist(self):
        playlist = Playlist.objects.create(name="Test Playlist")
        url = reverse('playlists-detail', kwargs={'uuid': playlist.uuid})
        data = {
            "name": "Test Playlist",
            "tracks": [
                {"track": self.track1.id, "order": 1}
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(playlist.tracks.count(), 1)

    def test_remove_track_from_playlist(self):
        playlist = Playlist.objects.create(name="Test Playlist")
        playlist.tracks.add(self.track1, through_defaults={'order': 1})
        playlist.tracks.add(self.track2, through_defaults={'order': 2})
        url = reverse('playlists-detail', kwargs={'uuid': playlist.uuid})
        data = {
            "name": "Test Playlist",
            "tracks": [
                {"track": self.track1.id, "order": 1}
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(playlist.tracks.count(), 1)

    def test_reorder_tracks_in_playlist(self):
        playlist = Playlist.objects.create(name="Test Playlist")
        playlist.tracks.add(self.track1, through_defaults={'order': 1})
        playlist.tracks.add(self.track2, through_defaults={'order': 2})
        url = reverse('playlists-detail', kwargs={'uuid': playlist.uuid})
        data = {
            "name": "Test Playlist",
            "tracks": [
                {"track": self.track2.id, "order": 1},
                {"track": self.track1.id, "order": 2}
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(playlist.playlisttrack_set.get(track=self.track2).order, 1)
        self.assertEqual(playlist.playlisttrack_set.get(track=self.track1).order, 2)

    def test_invalid_playlist_uuid(self):
        url = reverse('playlists-detail', kwargs={'uuid': uuid.uuid4()})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_playlist_with_invalid_track(self):
        url = reverse('playlists-list')
        data = {
            "name": "Test Playlist",
            "tracks": [
                {"track": 9999, "order": 1}  # Non-existent track ID
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_playlist_with_duplicate_order(self):
        url = reverse('playlists-list')
        data = {
            "name": "Test Playlist",
            "tracks": [
                {"track": self.track1.id, "order": 1},
                {"track": self.track2.id, "order": 2}  # Duplicate order
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)