## Overview
Create a Django app that implements a catalogue of music. It should have a fully-functional Django 
admin interface, and a read-only REST API. It should contain these three related data models in admin:
1. `Artist`
2. `Album`
3. `Track`
## Goals
* Implement the ability to fetch, create, update, and delete playlists through the REST API. A playlist 
should have a `uuid`, a `name`, and contain 0 or more tracks from this catalogue. The tracks should be 
order-able in the playlist.

* Implement the ability to fetch, create, update, and delete playlists through the Django templates. A 
playlist should have a `uuid`, a `name`, and contain 0 or more tracks from this catalogue. The tracks 
should be order-able in the playlist.

* Implement the test cases in `tests/test_playlists.py`. The goal is to have no skipped or failing tests.
* Update the Django admin with the ability to browse and manage playlists.

# ---------------------------------------------
# Steps for setup and run project
# ---------------------------------------------

1. `clone project from` [here](https://github.com/Mahammadhusain/music_catalogue.git)
2. `make python virtual environment and activate it`.
3. `install project dependencies using` command `pip install -r requirements.txt`
4. `after sucessfull install dependencies run django server using` command `python manage.py runserver`


# ---------------------------------------------
# API's reference
# ---------------------------------------------
Rest Api's roots start from `http://127.0.0.1:8000/api/` 
## API's Endpoints

1. `"artists": "http://127.0.0.1:8000/api/artists/"` - Read-only
2. `"albums": "http://127.0.0.1:8000/api/albums/"` - Read-only
3. `"tracks": "http://127.0.0.1:8000/api/tracks/"` - Read-only
4. `"playlists": "http://127.0.0.1:8000/api/playlists/"` - Full CRUD Support


# ---------------------------------------------
# Playlist CRUD Django views reference
# ---------------------------------------------
Playlist CRUD roots start from `http://127.0.0.1:8000/`
## Playlist CRUD urls of django views

- `playlists/ [name='playlist_list']`
- `playlists/create/ [name='playlist_create']`
- `playlists/<uuid:uuid>/ [name='playlist_detail']`
- `playlists/<uuid:uuid>/update/ [name='playlist_update']`
- `playlists/<uuid:uuid>/delete/ [name='playlist_delete']` 


# ---------------------------------------------
# Technologies used
# ---------------------------------------------

## Frontend
- `Html`
- `Css`
- `Javascript`
- `Bootstrap = 5.3.3`

## Backend
- `Python = 3.11.1`
- `Django = 5.0.6`
- `Django rest framework 3.15.2`

## Database
- `sqlite3`
