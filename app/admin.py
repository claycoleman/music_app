from django.contrib import admin
from app.models import Genre, Track, Album, Artist, CustomUser

# Register your models here.
class GenreAdmin(admin.ModelAdmin):
    '''
        Admin View for Genre
    '''
    list_display = ('genre_title', 'genre_id', 'genre_parent_id', 'genre_handle')
    search_fields = ['genre_title']

class TrackAdmin(admin.ModelAdmin):
    '''
        Admin View for Track
    '''
    list_display = ('track_title', 'track_id', 'album')
    search_fields = ['track_title']


class AlbumAdmin(admin.ModelAdmin):
    '''
        Admin View for Album
    '''
    list_display = ('album_title', 'album_id', 'artist', 'album_handle')
    search_fields = ['album_title']


class ArtistAdmin(admin.ModelAdmin):
    '''
        Admin View for Artist
    '''
    list_display = ('artist_name', 'artist_id', 'artist_handle')
    search_fields = ['artist_name']

class CustomUserAdmin(admin.ModelAdmin):
    '''
        Admin View for CustomUser
    '''
    list_display = ('email', 'is_staff')
    search_fields = ['username']

admin.site.register(Genre, GenreAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(CustomUser, CustomUserAdmin)