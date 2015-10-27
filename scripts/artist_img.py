#!/usr/bin/env python
import requests
import os, sys

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'project.settings')

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from app.models import Artist, Album
from django.conf import settings
from unidecode import unidecode

# payload = {'api_key': settings.FMAKEY, 'limit': 2000}

# for artist in Artist.objects.all():
#     payload.update({'artist_id': artist.artist_id})
#     response = requests.get('https://freemusicarchive.org/api/get/artists.json', params=payload)
#     try:
#         response_dict = response.json()
#     except Exception, e:
#         print e
#         continue

#     print artist
#     for data in response_dict['dataset']:
#         try:
#             image_response = requests.get(str(unidecode(data.get('artist_image_file')))) 
#             temp_image = NamedTemporaryFile(delete=True)
#             temp_image.write(image_response.content)
#             artist.artist_image.save('%s.jpg' % artist.artist_handle, File(temp_image)) 
#             print 'yes'
#         except Exception, e:
#             print e
#             continue

payload = {'api_key': settings.FMAKEY, 'limit': 2000}

for album in Album.objects.all():
    print album.album_image.url
    if album.album_image.url.startswith('/media/album_image/album_image'):
        payload.update({'album_id': album.album_id})
        try:
            response = requests.get('https://freemusicarchive.org/api/get/albums.json', params=payload)
            response_dict = response.json()
        except Exception, e:
            print e
            continue

        print album
        for data in response_dict['dataset']:
            try:
                image_response = requests.get(str(unidecode(data.get('album_image_file')))) 
                temp_image = NamedTemporaryFile(delete=True)
                temp_image.write(image_response.content)
                album.album_image.save('%s.jpg' % album.album_handle, File(temp_image)) 
                print 'yes'
            except Exception, e:
                print e
                continue
    else:
        print 'sudah'