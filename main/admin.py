from django.contrib import admin
from main.models import Movies, MovieImage, FavMovies, Genre, Profile, Moderator
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class MovieImageInline(admin.TabularInline):
    model = MovieImage

class FavMoviesInline(admin.TabularInline):
    model = FavMovies

class MovieAdmin(admin.ModelAdmin):
    inlines = [MovieImageInline, FavMoviesInline]
    search_fields = ['name']

class ModeratorInline(admin.StackedInline):
    model = Moderator
    verbose_name_plural = 'moderator'

class ProfileInline(admin.StackedInline):
    model = Profile
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, ModeratorInline]

admin.site.register(Movies, MovieAdmin)
admin.site.register(Genre)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)