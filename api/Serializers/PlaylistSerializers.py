from rest_framework import serializers
from ..models import Artist, Album, Track, Playlist, PlaylistTrack

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

class PlaylistTrackSerializer(serializers.ModelSerializer):
    track_title = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = PlaylistTrack
        fields = ['track', 'order','track_title']
    
    def get_track_title(self,obj):
        return obj.track.title

class PlaylistSerializer(serializers.ModelSerializer):
    tracks = PlaylistTrackSerializer(many=True, source='playlisttrack_set')

    class Meta:
        model = Playlist
        fields = ['uuid', 'name', 'tracks']

    def validate_tracks(self, value):
        orders = [track['order'] for track in value]
        if len(orders) != len(set(orders)):
            raise serializers.ValidationError("Track orders must be unique within a playlist.")
        return value

    def create(self, validated_data):
        tracks_data = validated_data.pop('playlisttrack_set')
        playlist = Playlist.objects.create(**validated_data)
        for track_data in tracks_data:
            PlaylistTrack.objects.create(playlist=playlist, **track_data)
        return playlist

    def update(self, instance, validated_data):
        tracks_data = validated_data.pop('playlisttrack_set')
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        
        instance.playlisttrack_set.all().delete()
        for track_data in tracks_data:
            PlaylistTrack.objects.create(playlist=instance, **track_data)
        return instance
    

