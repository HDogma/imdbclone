from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from watson import search as watson
import datetime

fs = FileSystemStorage(location=settings.MEDIA_ROOT)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(storage=fs, blank=True)
    biography = models.TextField(max_length=3000, blank=True)

    def __str__(self):
        return "Profile {email}".format(
            email=self.user.email
        )


class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_moderator = models.BooleanField()

    def __str__(self):
        return self.user.email


class Movies(models.Model):
    name = models.CharField(max_length=90)
    description = models.TextField(max_length=4000)
    description_short = models.CharField(max_length=80)
    logo = models.ImageField(storage=fs)
    created_at = models.DateField()
    video_url = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "Movie {name} - {year}".format(
            name=self.name,
            year=self.created_at
        )

    def update_movies_index(instance, **kwargs):
        for movies in instance.movies_set.all():
            watson.default_search_engine.update_obj_index(movies)

    @property
    def rating(self):
        p = MovieRating.objects.filter(movie=self).aggregate(Avg('rating'))
        p1 = str(p)
        p2 = p1.split(':')[1]
        p2 = p2.split('}')[0]
        if p2 == ' None':
            return 'None'
        else:
            return p2

    @property
    def votes(self):
        return MovieRating.objects.filter(movie=self).count()


class FavMovies(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movie = models.OneToOneField(Movies, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["movie", "user"]


class Genre(models.Model):
    name = models.CharField(max_length=90)

    def __str__(self):
        return "{name}".format(
            name=self.name
        )


class MovieRating(models.Model):
    NEUTRAL = 0
    VERY_BAD = 1
    BAD = 2
    OK = 3
    GOOD = 4
    VERY_GOOD = 5
    RATING_CHOICES = (
        (NEUTRAL, '0'),
        (VERY_BAD, '1'),
        (BAD, '2'),
        (OK, '3'),
        (GOOD, '4'),
        (VERY_GOOD, '5'),
    )
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES, default=NEUTRAL)

    class Meta:
        unique_together = ["movie", "user"]


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["movie", "genre"]


class Comments(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=3000, blank=True)
    is_moderatored = models.BooleanField()



class MovieImage(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return "{image}".format(
        image = self.image
    )


