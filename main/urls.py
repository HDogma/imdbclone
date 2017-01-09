from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^movie/new', views.addMovie, name='addMovie'),
    url(r'^movie/(?P<movie_id>[0-9]+)/comment/(?P<comment_id>[0-9]+)/edit', views.commentEdit, name='commentEdit'),
    url(r'^movie/(?P<movie_id>[0-9]+)/comment', views.comment, name='comment'),
    url(r'^movie/(?P<movie_id>[0-9]+)/media', views.addMoviesMedia, name='addMoviesMedia'),
    url(r'^movie/(?P<movie_id>[0-9]+)/like', views.like_movie, name='like_movie'),
    url(r'^movie/(?P<movie_id>[0-9]+)/unlike', views.unlike_movie, name='unlike_movie'),
    url(r'^movie/(?P<movie_id>[0-9]+)', views.showMovie, name='showMovie'),
    url(r'^profiles/(?P<user_id>[0-9]+)/contact', views.profile_contact, name='profile_contact'),
    url(r'^profile/(?P<movie_id>[0-9]+)/delete', views.unlike_movie, name='unlike_movie'),
    url(r'^profiles/(?P<user_id>[0-9]+)', views.profile_show, name='profile_show'),
    url(r'^profile/', views.profile_edit, name='profile_edit'),
    url(r'^search/', include("watson.urls", namespace="watson")),
    url(r'^imprint/', views.imprint, name='imprint'),
    url(r'^legal/', views.legal, name='legal'),
]