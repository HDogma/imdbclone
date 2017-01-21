from allauth.account.decorators import verified_email_required
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory, FileInput
from django.contrib.syndication.views import Feed
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from main.forms import MovieForm, ContactForm, ProfileEditForm, CommentsForm, CommentsEditForm, MovieRatingForm
from main.models import Movies, MovieImage, FavMovies, Comments, Genre, MovieGenre, MovieRating
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse



def home(request):
    """
        The Homepage
    """
    context = {
        "movies": Movies.objects.all(),
    }
    return render(request=request, template_name='main/home.html', context=context)


def showMovie(request, movie_id):
    if not request.user.is_authenticated() or not request.user.moderator.is_moderator:
        movie = get_object_or_404(Movies, id=movie_id)
        context = {
            'movie': movie,
            'comment_form': CommentsForm(),
            'fav': FavMovies.objects.filter(user__id=request.user.id, movie__id=movie_id),
            'rating': MovieRatingForm(),
        }
        return render(request, template_name='main/movie_show.html', context=context)
    else:
        if request.user.moderator.is_moderator:
            movie = get_object_or_404(Movies, id=movie_id)
            context = {
                'movie': movie,
                'comment_form': CommentsForm(),
                'comment_edit': CommentsEditForm(),
                'fav': FavMovies.objects.filter(user__id=request.user.id, movie__id=movie_id),
                'rating': MovieRatingForm(),
            }
            return render(request, template_name='main/movie_show.html', context=context)


def profile_show(request, user_id):
    """
        Profile page
    """
    user = get_object_or_404(User, id=user_id)
    context = {
        'user': user,
        'contactform' : ContactForm(),
        'fav': FavMovies.objects.filter(user__id=user_id)
    }
    return render(request, 'main/profile_show.html', context)


def profile_contact(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        contact_form = ContactForm(request.POST)
        print('1')
        if contact_form.is_valid():
            body = render_to_string(
                template_name='email/contactmessage.txt',
                context={
                    'name': user.get_full_name(),
                    'sender': contact_form.cleaned_data['name'],
                    'sender_email': contact_form.cleaned_data['email'],
                    'message': contact_form.cleaned_data['message']
                }
            )
            email = EmailMessage(
                subject = contact_form.cleaned_data['subject'],
                body = body,
                to = [user.email, contact_form.cleaned_data['email']],
                from_email =  'python@imdb.advanced'
            )
            email.send()
            messages.success(request, "E-Mail erfolgreich gesendet!")
            return redirect("profile_show", user_id)
        else:
            messages.error(request, "Ihre E-Mail konnte nicht gesendet werden!")
            return render(request, 'main/movie_new.html', {'contact_form': contact_form})
    else:
        print('2')
        return redirect("profile_show", user_id)


@login_required
def profile_edit(request):
    """
        Profile Edit Page
    """
    if request.method == 'POST':
        profileedit_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if profileedit_form.is_valid():
            profileedit_form.save()
            messages.success(request, 'Ihre Änderungen wurden erfolgreich gespeichert.')
            return redirect('profile_edit')
        else:
            print(profileedit_form.errors.as_data())
            messages.error(request, 'Fehler beim Speichern Ihrer Änderungen.')
            return redirect('profile_edit')
    else:
        context = {
            'profileedit_form': ProfileEditForm(instance=request.user.profile),
            'fav': FavMovies.objects.filter(user__id=request.user.id),
        }
        return render(request=request, template_name='main/profile_edit.html', context=context)


@verified_email_required
def addMovie(request):
    if request.method == 'POST':
        movie_form = MovieForm(request.POST, request.FILES)
        if movie_form.is_valid():
            movie = Movies.objects.create(
                name = movie_form.cleaned_data['name'],
                description = movie_form.cleaned_data['description'],
                description_short = movie_form.cleaned_data['description_short'],
                logo = request.FILES['logo'],
                created_at = movie_form.cleaned_data['created_at'],
                video_url = movie_form.cleaned_data['video_url']
            )
            messages.success(request, 'Film wurde erfolgreich angelegt.')
            return redirect('addMoviesMedia', movie.id)
        else:
            messages.error(request, 'Fehler beim Speichern des Filmes. Bitte überprüfen Sie alle Felder.')
            return render(request, 'main/movie_new.html', {'movie_form': movie_form})
    else:
        context = {
            'movie_form': MovieForm(),
        }
        return render(request=request, template_name='main/movie_new.html', context=context)


def addMoviesMedia(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)
    ImageFormSet = inlineformset_factory(Movies, MovieImage, fields=('image',), widgets={'image': FileInput()},
                                         can_delete=True, extra=1)
    if request.method == 'POST':
        formset = ImageFormSet(request.POST, request.FILES, instance=movie)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Bilder wurden erfolgreich Hinzugefügt.')
            return redirect('showMovie', movie.id)
        else:
            messages.error(request, 'Fehler beim Speichern des Filmes. Bitte überprüfen Sie alle Felder.')
            return render(request, 'main/movie_media.html', {'formset': formset})
    else:
        context = {
            'movie': movie,
            'formset': ImageFormSet(instance=movie),
        }
        return render(request=request, template_name='main/movie_media.html', context=context)

@login_required
def comment(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)
    if request.method == 'POST':
        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            Comments.objects.create (
                comment = comment_form.cleaned_data['comment'],
                is_moderatored = False,
                user = request.user,
                movie = movie
            )
            messages.success(request, 'Erfolgreich kommentiert.')
            return redirect('showMovie', movie.id)
        else:
            messages.error(request, 'Fehler beim Speichern Ihres Kommentares.')
            return render(request, 'main/movie_show.html', {'comment_form': comment_form})
    else:
        return redirect('showMovie', movie_id)


@login_required
def commentEdit(request, movie_id, comment_id):
    movie = get_object_or_404(Movies, id=movie_id)
    if request.method == 'POST':
        comment_form = CommentsForm(request.POST)
        comment = get_object_or_404(Comments, id=comment_id)
        if comment_form.is_valid():
            comment.comment = comment_form.cleaned_data['comment']
            comment.is_moderatored = True
            comment.save()
            messages.success(request, 'Erfolgreich editiert.')
            return redirect('showMovie', movie.id)
        else:
            messages.error(request, 'Fehler beim Editieren Ihres Kommentares.')
            return render(request, 'main/movie_show.html', {'comment_form': comment_form})
    else:
        return redirect('showMovie', movie_id)


@login_required
def rate_movie(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)
    if request.method == 'POST':
        rating_form = MovieRatingForm(request.POST)
        if rating_form.is_valid():
            if request.user in [movierating.user for movierating in movie.movierating_set.all()]:
                messages.error(request, 'Sie haben schon eine Bewertung abgegeben.')
                return redirect('showMovie', movie.id)
            else:
                MovieRating.objects.create(
                    movie = movie,
                    user = request.user,
                    rating = rating_form.cleaned_data['rating']
                )
                messages.success(request, 'Erfolgreich bewertet.')
                return redirect('showMovie', movie.id)
        else:
            return redirect('showMovie', movie.id)
    else:
        return redirect('showMovie', movie.id)






@login_required
def unlike_movie(request, movie_id):
    try:
        movie = get_object_or_404(Movies, id=movie_id)
        fav = FavMovies.objects.get(user=request.user, movie=movie)
        fav.delete()
        messages.success(request, "Sie favorisieren den Film nicht mehr.")
        return redirect('showMovie', movie_id)
    except:
        messages.error(request, "Ein Fehler ist aufgetretten, bitte versuchen Sie es noch einmal.")
        return redirect('showMovie', movie_id)


@login_required
def like_movie(request, movie_id):
    try:
        movie = get_object_or_404(Movies, id=movie_id)
        FavMovies.objects.create(
            user=request.user,
            movie=movie
        )
        messages.success(request, "Sie haben den Film erfolgreich favorisiert.")
        return redirect('showMovie', movie_id)
    except:
        messages.error(request, "Ein Fehler ist aufgetretten, bitte versuchen Sie es noch einmal.")
        return redirect('showMovie', movie_id)


def imprint(request):
    return render(request=request, template_name='main/imprint.html')


def legal(request):
    return render(request=request, template_name='main/legal.html')


class LatestMovieFeed(Feed):
    title = "Neuesten Filme"
    link = "/rss/"
    description = "Die neuesten Filme werden hier angezeigt."

    def items(self):
        return Movies.objects.order_by('-created_at')[:5]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return reverse('showMovie', args=[item.pk])