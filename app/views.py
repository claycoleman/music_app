import requests, urllib
from lxml import html
from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from app.models import Genre, Album, Artist, Track, CustomUser
from app.forms import UserLogin, UserSignUp, Search, ContactForm
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings


def genre_list(request):
    context = {}
    parent_genres = Genre.objects.filter(genre_parent_id=None)
    p = Paginator(parent_genres, 16)
    context['is_paginated'] = p.num_pages > 1
    context['paginator'] = p
    page_no = request.GET.get('page')
    if page_no != None and int(page_no) <= p.num_pages:
        context['page_obj'] = p.page(request.GET.get('page'))
    else:
        context['page_obj'] = p.page(1)
    context['genres'] = context['page_obj'].object_list

    return render_to_response('genre_list.html', context, context_instance=RequestContext(request))


class GenreListView(ListView):
    """docstring for GenresListView"""
    model = Genre
    template_name = 'genre_list.html'
    context_object_name = 'genres'
    paginate_by = 24

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GenreListView, self).get_context_data(**kwargs)
        context['parent_genres'] = Genre.objects.filter(genre_parent_id=None)
        return context


class GenreDetailView(DetailView):
    """docstring for GenreDetailView"""
    model = Genre
    template_name = 'genre_detail.html'
    slug_field = 'genre_handle'
    context_object_name = 'genre'



def genre_detail(request, slug):
    context = {}
    genre = Genre.objects.get(genre_handle=slug)
    context['genre'] = genre

    tracks = genre.track_set.all()
    print len(tracks)
    p = Paginator(tracks, 78)
    context['is_paginated'] = p.num_pages > 1
    print context['is_paginated']
    context['paginator'] = p
    page_no = request.GET.get('page')
    if (page_no != None and page_no != "") and int(page_no) <= p.num_pages:
        context['page_obj'] = p.page(page_no)
    else:
        context['page_obj'] = p.page(1)
    context['tracks'] = context['page_obj'].object_list

    return render_to_response('genre_detail.html', context, context_instance=RequestContext(request))


class GenreCreateView(CreateView):
    """docstring for GenreCreateView"""
    model = Genre
    fields = '__all__'
    template_name = 'genre_create.html'
    success_url = '/genre_list/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print 'worked'    
        return super(GenreCreateView, self).form_valid(form)





# def album_list(request):
#     context = {}
    
#     if request.method == "POST":
#         form = Search(request.POST)
#         context['form'] = form
#         if form.is_valid():
#             search = form.cleaned_data['search']
#             albums = Album.objects.filter(album_title__icontains=search)
#             if len(albums) > 54:
#                 albums = albums[:54]
#                 context['valid'] = "Too many search results! Displaying just the first 54. Try a more specific search"
#             context['is_paginated'] = False
#             context['albums'] = albums
#     else:
#         p = Paginator(Album.objects.all(), 24)
#         context['is_paginated'] = p.num_pages > 1
#         context['paginator'] = p
#         page_no = request.GET.get('page')
#         if page_no != None and int(page_no) <= p.num_pages:
#             context['page_obj'] = p.page(request.GET.get('page'))
#             print p.page(request.GET.get('page'))
#         else:
#             print 'front'
#             context['page_obj'] = p.page(1)

        
#         form = Search()
#         context['form'] = form

#         context['albums'] = context['page_obj'].object_list
#     return render_to_response('album_list.html', context, context_instance=RequestContext(request))


class AlbumListView(ListView):
    """docstring for AlbumsListView"""
    model = Album
    template_name = 'album_list.html'
    context_object_name = 'albums'
    paginate_by = 24

    def get_queryset(self):
        if 'search' in self.request.GET:
            object_list = Album.objects.filter(album_title__icontains=self.request.GET['search'])
        else:  
            object_list = Album.objects.all()
        return object_list

  

class AlbumDetailView(DetailView):
    """docstring for AlbumDetailView"""
    model = Album
    template_name = 'album_detail.html'
    slug_field = 'album_handle'
    context_object_name = 'album'


class AlbumCreateView(CreateView):
    """docstring for AlbumCreateView"""
    model = Album
    fields = '__all__'
    template_name = 'album_create.html'
    success_url = '/album_list/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print 'worked'    
        return super(AlbumCreateView, self).form_valid(form)


class AlbumUpdateView(UpdateView):
    """docstring for AlbumUpdateView"""
    model = Album
    fields = ['album_title', 'album_type', 'album_tracks', 'album_image']
    template_name = 'album_update.html'
    success_url = '/album_list/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print 'worked'    
        return super(AlbumUpdateView, self).form_valid(form)


class ArtistListView(ListView):
    """docstring for ArtistsListView"""
    model = Artist
    template_name = 'artist_list.html'
    context_object_name = 'artists'
    paginate_by = 24

    def get_queryset(self):
        if 'search' in self.request.GET:
            object_list = Artist.objects.filter(artist_name__icontains=self.request.GET['search'])
        else:  
            object_list = Artist.objects.all()
        return object_list


class ArtistDetailView(DetailView):
    """docstring for ArtistDetailView"""
    model = Artist
    template_name = 'artist_detail.html'
    slug_field = 'artist_handle'
    context_object_name = 'artist'


class ArtistCreateView(CreateView):
    """docstring for ArtistCreateView"""
    model = Artist
    fields = '__all__'
    template_name = 'artist_create.html'
    success_url = '/artist_list/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print 'worked'    
        return super(ArtistCreateView, self).form_valid(form)


class ArtistUpdateView(UpdateView):
    """docstring for ArtistUpdateView"""
    model = Artist
    fields = ['artist_name', 'artist_bio', 'artist_website', 'artist_image']
    template_name = 'artist_update.html'
    success_url = '/artist_list/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print 'worked'    
        return super(ArtistUpdateView, self).form_valid(form)


class TrackListView(ListView):
    """docstring for TracksListView"""
    model = Album
    template_name = 'track_list.html'
    context_object_name = 'albums'
    paginate_by = 54

    def get_queryset(self):
        if 'search' in self.request.GET:
            object_list = Album.objects.filter(track__track_title__icontains=self.request.GET.get('search'))
        else:  
            object_list = Album.objects.all()
        return object_list


def track_detail(request, pk):
    context = {}
    track = Track.objects.get(pk=pk)
    context['track'] = track
    try:    
        page = requests.get(track.track_url)
        tree = html.fromstring(page.text)
    
        file_url = tree.xpath('//*[@id="content"]/div[2]/div[2]/div/div[1]/div[1]/div/span[3]/a[1]/@href')[0]
        context['file_url'] = file_url
    except Exception, e:
        print e
        context['file_url'] = "fail"

    return render_to_response('track_detail.html', context, context_instance=RequestContext(request))


class TrackDetailView(DetailView):
    """docstring for TrackDetailView"""
    model = Track
    template_name = 'track_detail.html'
    context_object_name = 'track'

    def as_view(self):

        return super(TrackDetailView, self)


class TrackCreateView(CreateView):
    """docstring for TrackCreateView"""
    model = Track
    fields = '__all__'
    template_name = 'track_create.html'
    success_url = '/track_list/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print 'worked'    
        return super(TrackCreateView, self).form_valid(form)


class TrackUpdateView(UpdateView):
    """docstring for TrackUpdateView"""
    model = Track
    fields = ['track_title', 'track_favorites', 'track_listens', 'track_duration']
    template_name = 'track_update.html'
    success_url = '/track_list/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        print 'worked'    
        return super(TrackUpdateView, self).form_valid(form)


def login_view(request):
    context = {}
    context['form'] = UserLogin(initial={'next_page': request.GET.get('next')})
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            next_page = form.cleaned_data['next_page']
            auth_user = authenticate(email=email, password=password)
            if auth_user is not None:
                login(request, auth_user)
                if next_page is not None:
                    return redirect(next_page)
                else:
                    return redirect('music')
            else:
                context['valid'] = "Invalid user"
        else:
            context['valid'] = "Please enter a username!"

    return render_to_response('login.html', context, context_instance=RequestContext(request))

def logout_view(request):
    logout(request)
    next = request.GET.get('next')
    if next is not None:
        return redirect(next)
    else:
        return redirect('music')


def signup_view(request):
    context = {}
    context['form'] = UserSignUp(initial={'next_page': request.GET.get('next')})
    if request.method == 'POST':
        form = UserSignUp(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            next_page = form.cleaned_data['next_page']
            if password != password2:
                context['valid'] = "The passwords didn't match!"
                return render_to_response('register.html', context, context_instance=RequestContext(request))
            try: 
                new_user = CustomUser.objects.create_user(email, password)
                auth_user = authenticate(email=email, password=password)
                login(request, auth_user)
                if next_page is not None:
                    return redirect(next_page)
                else:
                    return redirect('music')

            except IntegrityError, e:
                context['valid'] = "Invalid email, or it's already been used to sign up!"
        else:
            context['valid'] = form.errors

    return render_to_response('register.html', context, context_instance=RequestContext(request))


def home(request):
    context = {}
    context['num_albums'] = len(Album.objects.all())
    context['num_artists'] = len(Artist.objects.all())
    context['num_genres'] = len(Genre.objects.all())
    context['num_tracks'] = len(Track.objects.all())
    return render_to_response('home.html', context, context_instance=RequestContext(request))


def music(request):
    context = {}

    return render_to_response('music.html', context, context_instance=RequestContext(request))


def contact(request):
    context = {}

    if request.method == 'POST':
        form = ContactForm(request.POST)
        context['form'] = form
        print "hello"
        if form.is_valid():
            print 'yikes'
            send_mail("arc-fm: %s" % form.cleaned_data['name'], form.cleaned_data['message'] + "\n" + form.cleaned_data['phone'], form.cleaned_data['email'], [settings.EMAIL_HOST_USER], fail_silently=False)
            return render(request, 'thanks.html')
    else:
        form = ContactForm()
        context['form'] = form
    return render_to_response('contact.html', context, context_instance=RequestContext(request))

