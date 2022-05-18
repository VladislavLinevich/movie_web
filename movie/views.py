from pyexpat import model
from django.shortcuts import render
from django.views.generic.base import View
from .models import Movie
from django.views import generic

class MovieListView(generic.ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)

class MovieDetailView(generic.DetailView):
    """Отдельный фильм"""
    model = Movie