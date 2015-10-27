#!/usr/bin/env python

import requests
import os, sys

sys.path.append("..")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'project.settings')

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from app.models import Track, Album, Genre, Artist
from unidecode import unidecode
from datetime import datetime
from lxml import html

import django
django.setup()

for count, track in enumerate(Track.objects.all()):
    if track.track_url == None or track.track_url.startswith('https://freemusicarchive.org/music/download/'):
        response = requests.get('https://freemusicarchive.org/api/get/tracks.json?api_key=OVKCLNSMSGB35I89&track_id=%s&limit=1' % track.track_id)

        try:
            response_dict = response.json()
        except Exception, e:
            print e
            continue

        for data in response_dict['dataset']:
            # try:    
            #     page = requests.get(data.get('track_url'))
            #     tree = html.fromstring(page.text)
            
            #     file_url = tree.xpath('//*[@id="content"]/div[2]/div[2]/div/div[1]/div[1]/div/span[3]/a[1]/@href')[0]
            #     track.track_url = file_url
            #     print "%d: %s" % (count, file_url)
            #     track.save()
            # except Exception, e:
            #     print e
            if data.get('track_url'):
                try:
                    track.track_url = data.get('track_url')
                except Exception, e:
                    print e
                    track.track_url = "http://fail.us/mickey/"
            print "%d: %s" % (count, track.track_url)
        track.save()
    else:
        print "Sudah berdownload"

            
