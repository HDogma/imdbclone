from django import forms
from django.forms import FileInput
from tinymce.widgets import TinyMCE
import datetime
from datetimewidget.widgets import DateWidget
from main.models import Profile, Movies, Comments, Genre, MovieRating

DATE_FORMATS = [
    '%d.%m.%Y'
]


class ContactForm(forms.Form):
    email = forms.CharField(max_length=140, label='E-Mail', widget=forms.TextInput(attrs={'placeholder': 'E-Mail'}))
    subject = forms.CharField(max_length=400, label='Betreff', widget=forms.TextInput(attrs={'placeholder': 'Betreff'}))
    message = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={'placeholder': 'Geben Sie hier bitte Ihre Nachricht ein ...'}))
    name = forms.CharField(max_length=50, label='Name', widget=forms.TextInput(attrs={'placeholder': 'Name'}))


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='Vorname', widget=forms.TextInput(attrs={'placeholder': 'Vorname'}))
    last_name = forms.CharField(max_length=30, label='Nachname', widget=forms.TextInput(attrs={'placeholder': 'Nachname'}))

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        Profile.objects.create(
            user=user,
        )


class MovieForm(forms.Form):
    name = forms.CharField(
        max_length=Movies._meta.get_field('name').max_length,
        label="Filmname*"
    )
    description = forms.CharField(
        max_length=Movies._meta.get_field('description').max_length,
        label="Beschreibung*",
        widget=TinyMCE
    )
    description_short = forms.CharField(
        max_length=Movies._meta.get_field('description_short').max_length,
        label="Kurzbeschreibung*"
    )
    logo = forms.ImageField(
        label='Logo*'
    )
    created_at = forms.DateField(
        input_formats=DATE_FORMATS,
        label='Erscheinungsdatum*',
        widget=DateWidget(usel10n=True, bootstrap_version=3)
    )
    video_url = forms.CharField(
        max_length=Movies._meta.get_field('video_url').max_length,
        label="Video URL (YouTube)",
        required=False
    )

class CommentsForm(forms.ModelForm):

    comment = forms.CharField(max_length=3000, label='Kommentar', widget=TinyMCE(attrs={'cols':70, 'rows': 5, 'placeholder': 'Geben Sie hier Ihr Kommentar ein...'}), required=False)

    class Meta:
        model = Comments
        fields = ['comment']


class CommentsEditForm(forms.ModelForm):

    comment = forms.CharField(max_length=3000, label='Kommentar', widget=TinyMCE(attrs={'rows': 2, 'placeholder': 'Geben Sie hier das neue Kommentar ein...'}), required=False)

    class Meta:
        model = Comments
        fields = ['comment']


class ProfileEditForm(forms.ModelForm):

    biography = forms.CharField(max_length=3000, label='Biographie', widget=TinyMCE(attrs={'cols':80, 'placeholder': 'Erzählen Sie etwas über sich hier...'}), required=False)
    picture = forms.ImageField(label='Profilbild', required=False)

    class Meta:
        model = Profile
        fields = ['biography', 'picture']


class MovieRatingForm(forms.ModelForm):

    rating = forms.ChoiceField(choices = MovieRating.RATING_CHOICES, label="", initial='', widget=forms.Select(), required=False)

    class Meta:
        model = MovieRating
        fields = ['rating']