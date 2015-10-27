#!/usr/bin/env python

import requests
import os, sys

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'project.settings')

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from app.models import Album, Artist
from unidecode import unidecode
from datetime import datetime

import django
django.setup()

for artist in Artist.objects.all():

    response = requests.get('https://freemusicarchive.org/api/get/albums.json?api_key=OVKCLNSMSGB35I89&artist_id=%s&limit=100' % artist.artist_id)
    
    try:
        response_dict = response.json()
    except Exception, e:
        print e
        continue

    print artist.artist_name

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
        
            new_album.artist = artist
            
            print new_album.album_title
            new_album.save()
