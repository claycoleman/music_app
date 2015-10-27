#!/usr/bin/env python

import requests
import os, sys

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'project.settings')

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from app.models import Artist
from unidecode import unidecode

import django
django.setup()

response = requests.get('https://freemusicarchive.org/api/get/artists.json?api_key=OVKCLNSMSGB35I89&limit=2000')

response_dict = response.json()

for data in response_dict['dataset']:
    new_artist, created = Artist.objects.get_or_create(artist_id=int(data['artist_id']))

    if data['artist_bio']!= None:
        new_artist.artist_bio = str(unidecode(data.get('artist_bio', "")))
    new_artist.artist_handle = str(unidecode(data.get('artist_handle', "")))
    new_artist.artist_name = str(unidecode(data.get('artist_name', "")))
    
    if data.get('artist_members')!=None:
        new_artist.artist_members = str(unidecode(data.get('artist_members')))
    if data.get('artist_website')!=None:
        new_artist.artist_website = str(unidecode(data.get('artist_website', "")))
    if data.get('artist_wikipedia_page') != None:
        new_artist.artist_wikipedia_page = str(unidecode(data.get('artist_wikipedia_page', "")))
    if data.get('artist_active_year_begin')!= None:
        new_artist.artist_active_year_begin = str(unidecode(data.get('artist_active_year_begin', "")))
    if data.get('artist_active_year_end')!= None:
        new_artist.artist_active_year_end = str(unidecode(data.get('artist_active_year_end')))
    new_artist.artist_comments = int(data.get('artist_comments', 0))
    new_artist.artist_favorites = int(data.get('artist_favorites', 0))
    if data.get('artist_latitude')!= None:
        new_artist.artist_latitude = str(unidecode(data.get('artist_latitude', " ")))
    if data.get('artist_longitude')!= None:
        new_artist.artist_longitude = str(unidecode(data.get('artist_longitude', " ")))

    try:
        image_response = requests.get(str(unidecode(data.get('artist_image_file')))) 
        temp_image = NamedTemporaryFile(delete=True)
        temp_image.write(image_response.content)
        new_artist.artist_image.save('artist_image.jpg', File(temp_image)) 
    except Exception, e:
        print e

    new_artist.save()
