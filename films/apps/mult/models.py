from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    gender = models.BooleanField(verbose_name="пол", default=None, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default="avatars/default_user.png")

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Film(models.Model):
    name = models.TextField('Название фильма', default="Название")
    country = models.CharField('Страна', max_length=150, default="США")
    seasons = models.CharField('Количество сезонов', max_length=50, default="1")
    filmtype = models.CharField('Тип', max_length=20, default="Фильм")
    year = models.CharField('Год выпуска', max_length=10, default="2020")
    description = models.TextField('Описаное', default="НЕТУ")
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр для фильма", verbose_name="Жанр", blank=True)
    img = models.ImageField(upload_to="images/films", default="static/mult/image/default.jpg", blank=True, null=True)
    img_url = models.TextField('ссылка на исходную картинку')
    unformated_name = models.TextField("Имя папки", default=name)
    mult = models.BooleanField("Является ли мультиком", default=False)
    isShown = models.BooleanField("Показывать ли на странице", default=True)
    create_date = models.DateTimeField("Дата создания", auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='film_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='film_dislikes')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['name']


class SeriesFilms(models.Model):
    name = models.ForeignKey(Film, on_delete=models.CASCADE)
    name_serie = models.TextField('Название серии')
    href = models.TextField('Ссылка на серию')
    full_name = models.TextField('Полное название серии')

    def __str__(self):
        return self.name_serie

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии Фильмов'
        ordering = ['name_serie']


class Mult(models.Model):
    name = models.TextField('Название мультика')
    episodes = models.TextField('Количество эпизодов')
    status = models.TextField('Вышло или нет')
    description = models.TextField('Описаное')
    img_url = models.TextField('Картинка')
    img = models.ImageField(upload_to="images/mults", default="static/mult/image/default.jpg", blank=True, null=True)
    genre = models.ManyToManyField(Genre, help_text="Выберите жанр для мультика", verbose_name="Жанр", blank=True)
    unformated_name = models.TextField("Имя папки")
    mult = models.BooleanField("Является ли мультиком", default=True)
    isShown = models.BooleanField("Показывать ли на странице", default=True)
    create_date = models.DateTimeField("Дата создания", auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='mult_likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='mult_dislikes')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Мультфильм'
        verbose_name_plural = 'Мультфильмы'
        ordering = ['name']


class Series(models.Model):
    name = models.ForeignKey(Mult, on_delete=models.CASCADE)
    name_serie = models.TextField('Название серии')
    href = models.TextField('Ссылка на серию')
    full_name = models.TextField('Полное название серии')

    def __str__(self):
        return self.name_serie

    class Meta:
        verbose_name = 'Серия'
        verbose_name_plural = 'Серии Мультфильмов'
        ordering = ['name_serie']


class Subs(models.Model):
    name = models.ForeignKey(Series, on_delete=models.CASCADE)
    mult = models.ForeignKey(Mult, on_delete=models.CASCADE)
    name_sub = models.TextField('Название субтитра')
    autor = models.TextField('Автор субтитров')
    href = models.TextField('Ссылка на субтитр')

    def __str__(self):
        return self.name_sub

    class Meta:
        verbose_name = 'Субтитры'
        verbose_name_plural = 'Субтитры Мультфильмов'
        ordering = ['name_sub']


class Audio(models.Model):
    name = models.ForeignKey(Series, on_delete=models.CASCADE)
    mult = models.ForeignKey(Mult, on_delete=models.CASCADE)
    name_audio = models.TextField('Название озвучки')
    autor = models.TextField('Автор озвучки')
    href = models.TextField('Ссылка на озвучку')

    def __str__(self):
        return self.name_audio

    class Meta:
        verbose_name = 'Озвучка'
        verbose_name_plural = 'Озвучка Мультфильмов'
        ordering = ['name_audio']
