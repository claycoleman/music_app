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
from lxml import html

import django
django.setup()

payload = {'api_key': settings.FMAKEY, 'limit': 2000}

for artist in Artist.objects.all():
    payload.update({'artist_id': artist.artist_id})
    response = requests.get('https://freemusicarchive.org/api/get/albums.json', params=payload)
    try:
        response_dict = response.json()
    except Exception, e:
        print e
        continue

    for data in response_dict['dataset']:
        if len(data) is not 0:
            new_album, created = Album.objects.get_or_create(album_id=int(data['album_id']))

            if data.get('album_handle') != None:
                new_album.album_handle = str(unidecode(data.get('album_handle', "")))
            if data.get('album_title') != None:
                new_album.album_title = str(unidecode(data.get('album_title', "")))
            if data.get('album_type') != None:
                new_album.album_type = str(unidecode(data.get('album_type', "")))
            if data.get('album_information') != None:
                new_album.album_information = str(unidecode(data.get('album_information', "")))
            if data.get('album_date_released') != None:
                date = str(unidecode(data.get('album_date_released', "")))
                new_date = datetime.strptime(date, "%m/%d/%Y").date()
                new_album.album_date_released = new_date
            new_album.album_comments = int(data.get('album_comments', ""))
            new_album.album_favorites = int(data.get('album_favorites', ""))
            new_album.album_tracks = int(data.get('album_tracks', ""))
            new_album.album_listens = int(data.get('album_listens', ""))
            try:
                image_response = requests.get(str(unidecode(data.get('album_image_file')))) 
                temp_image = NamedTemporaryFile(delete=True)
                temp_image.write(image_response.content)
                new_album.album_image.save('album_image.jpg', File(temp_image)) 
            except Exception, e:
                print e
                continue
        
            new_album.artist = artist

            print new_album.album_title

            payer = {'api_key': settings.FMAKEY, 'limit': 200, 'album_id': new_album.album_id}

            respon = requests.get('https://freemusicarchive.org/api/get/tracks.json', params=payer)

            try:
                respon_dict = respon.json()
            except Exception, e:
                print e
                continue
            
            for dete in respon_dict['dataset']:
                new_track, created = Track.objects.get_or_create(track_id=int(dete['track_id']))

                if dete.get('track_title') != None:
                    new_track.track_title = str(unidecode(dete.get('track_title', "")))
                if dete.get('track_type') != None:     
                    new_track.track_type = str(unidecode(dete.get('track_type', "")))
                if dete.get('track_information') != None:
                    new_track.track_information = str(unidecode(dete.get('track_information', "")))

                new_track.album = new_album
                if dete.get('track_genres'):
                    genres = dete['track_genres']
                for diction in genres:
                    new_track.genre.add(Genre.objects.get(genre_id=diction['genre_id']))

                if dete.get('track_title') != None:
                    new_track.track_title = str(unidecode(dete.get('track_title')))
                new_track.track_favorites = int(dete.get('track_favorites', ""))
                new_track.track_listens = int(dete.get('track_listens', ""))
                new_track.track_interest = int(dete.get('track_interest'))

                if dete.get('track_duration') != None:
                    new_track.track_duration = str(unidecode(dete.get('track_duration')))

                print new_track.track_title
   
                new_track.track_url = dete.get('track_url'))
                new_track.save()


            new_album.save()
