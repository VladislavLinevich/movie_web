from datetime import date
from tabnanny import verbose
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from embed_video.fields import EmbedVideoField


class Category(models.Model):
    name = models.CharField("Категории", max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Actor(models.Model):
    name = models.CharField("Имя", max_length=30)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.URLField("Изображение")

    def __str__(self):
        return self.name

    def get_image(self):
        return mark_safe(f'<img src={self.image} width="80" height="90"')

    get_image.short_description = "Фото"

    def get_absolute_url(self):
        return reverse('actor-detail', args=[str(self.id)])

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"


class Movie(models.Model):
    """Фильм"""
    date_creation = models.DateTimeField("Дата добавления", auto_now_add=True)
    title = models.CharField("Название", max_length=80, db_index=True)
    tagline = models.CharField("Слоган", max_length=80, default='')
    description = models.TextField("Описание")
    poster = models.URLField("Постер")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=20)
    directors = models.ManyToManyField(Actor, verbose_name="режиссер", related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="актеры", related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premiere = models.DateField("Примьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0,
                                         help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="указывать сумму в долларах"
    )
    fess_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указывать сумму в долларах"
    )
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    draft = models.BooleanField("Черновик", default=False)
    video = EmbedVideoField(blank=True, verbose_name='Видео')

    def display_genre(self):
        """Создание строки жанров"""
        return ', '.join([genre.name for genre in self.genres.all()])

    display_genre.short_description = 'Жанр'

    def get_poster(self):
        return mark_safe(f'<img src={self.poster} width="80" height="90"')

    get_poster.short_description = "Постер"

    def display_director(self):
        """Создание строки режиссеров"""
        return ', '.join([director.name for director in self.directors.all()])

    display_director.short_description = 'Режиссеры'

    def display_actor(self):
        """Создание строки актеров"""
        return ', '.join([actor.name for actor in self.actors.all()])

    display_actor.short_description = 'Актеры'

    def get_absolute_url(self):
        return reverse('movie-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class Reviews(models.Model):
    """Отзывы"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField("Сообщение", max_length=5000)
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
