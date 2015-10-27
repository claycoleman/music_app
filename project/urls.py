"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.edit import CreateView
from app.forms import CustomUserCreateForm
from django.contrib.auth import views as auth_views


urlpatterns = [
    url(r'^nimda/', include(admin.site.urls)),
    url(r'^$', 'app.views.home', name='home'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^music/genre_list/$', 'app.views.genre_list', name='genre_list'),
    # url(r'^genre_detail/(?P<pk>\d+)/$', views.GenreDetailView.as_view(), name='genre_detail'),
    url(r'^music/genre_detail/(?P<slug>.+)/$', "app.views.genre_detail", name='genre_detail'),
    # url(r'^music/genre_detail/(?P<slug>.+)/$', views.GenreDetailView.as_view(), name='genre_detail'),
    url(r'^music/album_list/$', views.AlbumListView.as_view(), name='album_list'),
    # url(r'^music/album_list/$', 'app.views.album_list', name='album_list'),
    url(r'^music/album_detail/(?P<slug>.+)/$', views.AlbumDetailView.as_view(), name='album_detail'),
    url(r'^music/artist_list/$', views.ArtistListView.as_view(), name='artist_list'),
    url(r'^music/artist_detail/(?P<slug>.+)/$', views.ArtistDetailView.as_view(), name='artist_detail'),
    url(r'^music/track_list/$', views.TrackListView.as_view(), name='track_list'),
    # url(r'^music/track_detail/(?P<pk>\d+)/$', views.TrackDetailView.as_view(), name='track_detail'),
    url(r'^music/track_detail/(?P<pk>\d+)/$', 'app.views.track_detail', name='track_detail'),
    # url(r'^music/create_genre/$', views.GenreCreateView.as_view(), name='create_genre'),
    # url(r'^music/create_artist/$', views.ArtistCreateView.as_view(), name='create_artist'),
    # url(r'^music/update_artist/(?P<pk>\d+)/$', views.ArtistUpdateView.as_view(), name='update_artist'),
    # url(r'^music/create_album/$', views.AlbumCreateView.as_view(), name='create_album'),
    # url(r'^music/update_album/(?P<pk>\d+)/$', views.AlbumUpdateView.as_view(), name='update_album'),
    # url(r'^music/create_track/$', views.TrackCreateView.as_view(), name='create_track'),
    # url(r'^music/update_track/(?P<pk>\d+)/$', views.TrackUpdateView.as_view(), name='update_track'),
    url(r'^log_in/$', 'app.views.login_view', name='login'),
    url(r'^log_out/$', 'app.views.logout_view', name='logout'),
    url(r'^signup/$', 'app.views.signup_view', name='signup'),
    url(r'^music/$', 'app.views.music', name='music'),
    url(r'^contact/$', 'app.views.contact', name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
