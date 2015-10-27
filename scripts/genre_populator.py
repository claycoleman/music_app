#!/usr/bin/env python
import requests
import os, sys

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'project.settings')

from app.models import Genre

response = requests.get('https://freemusicarchive.org/api/get/genres.json?api_key=OVKCLNSMSGB35I89&limit=170')

response_dict = response. json()

for data in response_dict['dataset']:
    new_genre, created = Genre.objects.get_or_create(genre_id=data['genre_id'])
    new_genre.genre_title = data['genre_title']
    new_genre.genre_handle = data['genre_handle']
    new_genre.genre_parent_id = data['genre_parent_id']

    new_genre.save()
