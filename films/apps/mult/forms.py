from django import forms
from .models import Genre, Film, User
from .parse import kinopoiskParse, shikimoriParse
from urllib.parse import urlsplit, urlunsplit
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class ListForm(forms.Form):
    ordering = forms.ChoiceField(label="сортировка", required=False, initial=["-name", "По убыванию"], choices=[
        ["name", "По алфавиту А-Я"],
        ["-name", "По алфавиту Я-А"],
        ["-create_date", "Сначала новые"],
        ["create_date", "Сначала старые"]
    ])
    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), label='жанры', empty_label="Выберите жанр",
                                   initial=1, required=False)


class AdminUrlForm(forms.ModelForm):
    kino_url = forms.URLField(label="Ссылка на Кинопоиск", required=False)

    def clean(self):
        kino_url = urlsplit(self.cleaned_data.get('kino_url', None))
        if kino_url.hostname:
            message = "В данный момент сайт недоступен"
            try:
                if kino_url.hostname == "www.kinopoisk.ru":
                    film = kinopoiskParse(film_id=kino_url.path.split("/")[2])
                elif kino_url.hostname == "shikimori.one":
                    film = shikimoriParse(urlunsplit(kino_url))
                else:
                    message = "Укажите ссылку на Кинопоиск или Шикимори"
                    raise ConnectionError
                self.cleaned_data['name'] = film['name']
                self.cleaned_data["episodes"] = film['episodes']
                self.cleaned_data["status"] = film['status']
                self.cleaned_data["isShown"] = True
                self.cleaned_data["img_url"] = film['img']
                self.cleaned_data["description"] = film['description']
                if self.cleaned_data['img']:
                    self.cleaned_data['img'].delete()
                self.cleaned_data['genre'] = [Genre.objects.get(name=genre) for genre in film['genre']]
                if self.Meta.model == Film:
                    self.cleaned_data['year'] = film['year']
                    self.cleaned_data['country'] = film['country']
                    self.cleaned_data['seasons'] = film['seasons']
                    self.cleaned_data['filmtype'] = film['type']
            except:
                raise ValidationError({"kino_url": message})
        return self.cleaned_data


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(label=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Имя пользователя', 'id': 'hello'}))
    password = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'id': 'hi',
        }))
    error_messages = {
        'invalid_login': "Неверное имя пользователя или пароль",
        'inactive': "Этот аккаунт заблокирован",
    }


class UserRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

    username = UsernameField(label=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))

    email = forms.EmailField(label=False, widget=forms.TextInput(
        attrs={'type': 'email',
               'placeholder': 'E-mail'}))
    password1 = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={
            'class': 'pass1',
            'placeholder': 'Пароль',
        }))

    password2 = forms.CharField(label=False, widget=forms.PasswordInput(
        attrs={
            'class': 'pass1',
            'placeholder': 'Повторите пароль',
        }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class UserChangeInfo(forms.ModelForm):
    username = UsernameField(label=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}))
    email = forms.EmailField(label=False, widget=forms.TextInput(
        attrs={'type': 'email',
               'placeholder': 'E-mail'}))
    class Meta:
        model = get_user_model()
        fields = ('username', 'email',)

# class UserChangeInfo(UserChangeForm):
#     username = UsernameField(label=False, widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Имя пользователя', 'id': 'hello'}))
#     email = forms.EmailField(label=False, widget=forms.TextInput(
#         attrs={'type': 'email',
#                'placeholder': 'E-mail'}))
#     # avatar = forms.ImageField(label=False)
#     class Meta:
#         model = get_user_model()
#         fields = ('username', 'email', 'avatar')
