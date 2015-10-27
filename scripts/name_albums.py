#!/usr/bin/env python
import requests
import os, sys

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'project.settings')

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from app.models import Album
from unidecode import unidecode
from datetime import datetime

import django
django.setup()

for album in Album.objects.all():
    if album.album_title == None:
        response = requests.get('https://freemusicarchive.org/api/get/albums.json?api_key=OVKCLNSMSGB35I89&album_id=%s&limit=100' % album.album_id)
    
        try:
            response_dict = response.json()
        except Exception, e:
            print e
            continue

        if len(response_dict['dataset']) is 0:
            album.delete()
            print "deleted!"
            continue
        else:
            print "Before: %s" % album.album_title
            for data in response_dict['dataset']:
                album.album_title = str(unidecode(data.get('album_title')))
            print "After: %s" % album.album_title
            album.save()

    if album.album_handle == None:
        response = requests.get('https://freemusicarchive.org/api/get/albums.json?api_key=OVKCLNSMSGB35I89&album_id=%s&limit=100' % album.album_id)
    
        try:
            response_dict = response.json()
        except Exception, e:
            print e
            continue

        else:
            print "Before: %s" % album.album_handle
            for data in response_dict['dataset']:
                album.album_handle = str(unidecode(data.get('album_handle')))
            print "After: %s" % album.album_handle
            album.save()
