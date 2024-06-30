from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from api.models import Playlist, Track, PlaylistTrack
from django.forms import formset_factory
from django.db import transaction
from django.forms import CheckboxInput

def playlist_list(request):
    playlists = Playlist.objects.all()
    return render(request, 'catalogue/playlist_list.html', {'playlists': playlists})


class TrackOrderForm(forms.Form):
    track = forms.ModelChoiceField(queryset=Track.objects.all(),empty_label="Select a track", widget=forms.Select({'class':'form-select'}))
    order = forms.IntegerField(min_value=0, widget=forms.NumberInput({'class':'form-control','placeholder':'Enter order no.'}))
    DELETE = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter playlist name'})
        }

PlaylistTrackFormSet = formset_factory(TrackOrderForm, extra=1, can_delete=True)

def playlist_create(request):
    if request.method == 'POST':
        playlist_form = PlaylistForm(request.POST)
        formset = PlaylistTrackFormSet(request.POST)
        if playlist_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                playlist = playlist_form.save()
                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        PlaylistTrack.objects.create(
                            playlist=playlist,
                            track=form.cleaned_data['track'],
                            order=form.cleaned_data['order']
                        )
            return redirect('playlist_detail', uuid=playlist.uuid)
    else:
        playlist_form = PlaylistForm()
        formset = PlaylistTrackFormSet()
    return render(request, 'catalogue/playlist_form.html', {
        'playlist_form': playlist_form,
        'formset': formset
    })

def playlist_update(request, uuid):
    playlist = get_object_or_404(Playlist, uuid=uuid)
    if request.method == 'POST':
        playlist_form = PlaylistForm(request.POST, instance=playlist)
        formset = PlaylistTrackFormSet(request.POST)
        if playlist_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                playlist_form.save()
                playlist.playlisttrack_set.all().delete()
                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        PlaylistTrack.objects.create(
                            playlist=playlist,
                            track=form.cleaned_data['track'],
                            order=form.cleaned_data['order']
                        )
            return redirect('playlist_detail', uuid=playlist.uuid)
    else:
        playlist_form = PlaylistForm(instance=playlist)
        initial_data = [
            {'track': pt.track, 'order': pt.order}
            for pt in playlist.playlisttrack_set.all().order_by('order')
        ]
        formset = PlaylistTrackFormSet(initial=initial_data)
    return render(request, 'catalogue/playlist_form.html', {
        'playlist_form': playlist_form,
        'formset': formset,
        'playlist': playlist
    })

def playlist_detail(request, uuid):
    playlist = get_object_or_404(Playlist, uuid=uuid)
    return render(request, 'catalogue/playlist_detail.html', {'playlist': playlist})


def playlist_delete(request, uuid):
    playlist = get_object_or_404(Playlist, uuid=uuid)
    if request.method == 'POST':
        playlist.delete()
        return redirect('playlist_list')
    return render(request, 'catalogue/playlist_confirm_delete.html', {'playlist': playlist})