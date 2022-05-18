from multiprocessing import context
from pyexpat import model
from django.shortcuts import render
from django.views.generic.base import View
from .models import Category, Movie, Actor
from django.views import generic

class MovieListView(generic.ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["movies"] = Movie.objects.filter(draft=False).order_by("id")[:4]
        context["categories"] = Category.objects.all()
        return context

class MovieDetailView(generic.DetailView):
    """Отдельный фильм"""
    model = Movie

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["movies"] = Movie.objects.filter(draft=False).order_by("id")[:4]
        context["categories"] = Category.objects.all()
        return context

class ActorDetailView(generic.DetailView):
    """Отдельный фильм"""
    model = Actor

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["movies"] = Movie.objects.filter(draft=False).order_by("id")[:4]
        context["categories"] = Category.objects.all()
        return context