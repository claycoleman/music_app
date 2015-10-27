#!/usr/bin/env python

import requests
import os, sys

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'project.settings')

from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from app.models import Track, Album, Genre, Artist
from unidecode import unidecode
from datetime import datetime

import django
django.setup()

payload = {'api_key': settings.FMAKEY, 'limit': 200}

artists = Artist.objects.all()
for album in Album.objects.all():
    if album.artist != None:
        print "excluded"
        artists = artists.exclude(artist_id=album.artist.artist_id)
    payload.update({'album_id': album.album_id})
    response = requests.get('https://freemusicarchive.org/api/get/tracks.json', params=payload)

    try:
        response_dict = response.json()
    except Exception, e:
        print e
        continue

    print "Album: %s" % album.album_id

    for data in response_dict['dataset']:
        new_track, created = Track.objects.get_or_create(track_id=int(data['track_id']))

        if data.get('track_title') != None:
            new_track.track_title = str(unidecode(data.get('track_title', "")))
        if data.get('track_type') != None:     
            new_track.track_type = str(unidecode(data.get('track_type', "")))
        if data.get('track_information') != None:
            new_track.track_information = str(unidecode(data.get('track_information', "")))

        new_track.album = album
        if data.get('track_genres'):
            genres = data['track_genres']
        for diction in genres:
            new_track.genre.add(Genre.objects.get(genre_id=diction['genre_id']))

        if data.get('track_title') != None:
            new_track.track_title = str(unidecode(data.get('track_title')))
        new_track.track_favorites = int(data.get('track_favorites', ""))
        new_track.track_listens = int(data.get('track_listens', ""))
        new_track.track_interest = int(data.get('track_interest'))

        if data.get('track_duration') != None:
            new_track.track_duration = str(unidecode(data.get('track_duration')))

        print new_track.track_title

        new_track.save()

        # try:
        #     track_response = requests.get(str(unidecode(data.get('track_file'))))
        #     temp_image = NamedTemporaryFile(delete=True)
        #     temp_image.write(image_response.content)
        #     new_album.track_file.save('track.mp3', File(temp_image))
        # except Exception, e:
        #         print e
for artist in artists:
    response = requests.get('https://freemusicarchive.org/api/get/tracks.json?api_key=OVKCLNSMSGB35I89&artist_id=%s&limit=200' % artist.artist_id)

    try:
        response_dict = response.json()
    except Exception, e:
        print e
        continue

    print "Artist: %s" % artist.artist_id

    for data in response_dict['dataset']:
        new_track, created = Track.objects.get_or_create(track_id=int(data['track_id']))

        if data.get('track_title') != None:
            new_track.track_title = str(unidecode(data.get('track_title', "")))
        if data.get('track_type') != None:     
            new_track.track_type = str(unidecode(data.get('track_type', "")))
        if data.get('track_information') != None:
            new_track.track_information = str(unidecode(data.get('track_information', "")))

        if data.get('album_id') != None:
            print data.get('album_id')
            new_album, created = Album.objects.get_or_create(album_id=data.get('album_id'))
            new_album.artist = artist
            new_track.album = new_album

            new_album.save()
        if data.get('track_genres'):
            genres = data['track_genres']
        for diction in genres:
            new_track.genre.add(Genre.objects.get(genre_id=diction['genre_id']))

        if data.get('track_title') != None:
            new_track.track_title = str(unidecode(data.get('track_title')))
        new_track.track_favorites = int(data.get('track_favorites', ""))
        new_track.track_listens = int(data.get('track_listens', ""))
        new_track.track_interest = int(data.get('track_interest'))

        if data.get('track_duration') != None:
            new_track.track_duration = str(unidecode(data.get('track_duration')))

        print new_track.track_title

        new_track.save()
print "Number of artists found: %d" % len(artists) 
