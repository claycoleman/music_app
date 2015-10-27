from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# class Curator(models.Model):
#     """
#     Description: Model Description
#     """
#     pass


class Genre(models.Model):
    """
    Description: Model Description
    """
    genre_id = models.IntegerField(null=True, blank=True)
    genre_parent_id = models.IntegerField(null=True, blank=True)
    genre_title = models.CharField(max_length=255, null=True, blank=True)
    genre_handle = models.SlugField(max_length=255, null=True, blank=True)
    parent_genre = models.ForeignKey('Genre', null=True, blank=True)

    def __unicode__(self):
        return self.genre_title

class Artist(models.Model):
    """
    Description: Model Description
    """
    artist_id = models.IntegerField(null=True, blank=True)
    artist_handle = models.SlugField(max_length=255, null=True, blank=True)
    artist_name = models.CharField(max_length=255, null=True, blank=True)
    artist_bio = models.TextField(null=True, blank=True)
    artist_members = models.TextField(null=True, blank=True)
    artist_website = models.URLField(null=True, blank=True)
    artist_wikipedia_page = models.URLField(null=True, blank=True)
    artist_active_year_begin = models.CharField(max_length=255, null=True, blank=True)
    artist_active_year_end = models.CharField(max_length=255, null=True, blank=True)
    artist_comments = models.IntegerField(null=True, blank=True)
    artist_favorites = models.IntegerField(null=True, blank=True)
    artist_latitude = models.CharField(max_length=255, null=True, blank=True)
    artist_longitude = models.CharField(max_length=255, null=True, blank=True)
    artist_image = models.ImageField(upload_to="artist_image", null=True, blank=True)

    def __unicode__(self):
        return self.artist_name

class Album(models.Model):
    album_id = models.IntegerField(null=True, blank=True)
    album_title = models.CharField(max_length=255, null=True, blank=True)
    album_handle = models.SlugField(max_length=255, null=True, blank=True)
    artist = models.ForeignKey('app.Artist', null=True, blank=True)
    album_type = models.CharField(max_length=255, null=True, blank=True)
    album_information = models.TextField(null=True, blank=True)
    album_date_released = models.DateField(null=True, blank=True)
    album_comments = models.IntegerField(null=True, blank=True)
    album_favorites = models.IntegerField(null=True, blank=True)
    album_tracks = models.IntegerField(null=True, blank=True)
    album_listens = models.IntegerField(null=True, blank=True)
    album_image = models.ImageField(upload_to='album_image', null=True, blank=True)

    class Meta:
        ordering = ['album_title']

    def __unicode__(self):
        return self.album_title

class Track(models.Model):
    """
    Description: Model Description
    """
    track_id = models.IntegerField(null=True, blank=True)
    album = models.ForeignKey('app.Album', null=True, blank=True)
    genre = models.ManyToManyField('app.Genre', blank=True)
    track_title = models.CharField(max_length=255, null=True, blank=True)
    track_favorites = models.IntegerField(null=True, blank=True) 

    track_listens = models.IntegerField(null=True, blank=True)
    track_interest = models.IntegerField(null=True, blank=True)
    track_duration = models.CharField(max_length=255, null=True, blank=True)
    track_url = models.URLField(max_length=500, null=True, blank=True)

    def __unicode__(self):
        return self.track_title


class CustomUserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()

        if not email:
            email = username
        email = self.normalize_email(email)
        user = self.model(email=email,
                              is_staff=is_staff,
                              is_active=True,
                              is_superuser=is_superuser,
                              last_login=now,
                              date_joined=now,
                              **extra_fields
                              )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user("", email, password, False, False, **extra_fields)     


    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', max_length=255, unique=True)
    first_name = models.CharField('first_name', max_length=255, blank=True, null=True)
    last_name = models.CharField('last name', max_length=255, blank=True, null=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name ='user'
        verbose_name_plural = 'users'

    def __unicode__(self):
        return self.email.partition('@')[0]

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

