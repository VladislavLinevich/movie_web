from multiprocessing import context
from pyexpat import model
from django.shortcuts import render
from django.views.generic.base import View
from .models import Category, Movie, Actor, Genre
from django.views import generic
from django.db.models import Q

class MovieListView(generic.ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["last_movies"] = Movie.objects.filter(draft=False).order_by("-id")[:4]
        context["categories"] = Category.objects.all()
        context["genres"] = Genre.objects.all()
        context["years"] = Movie.objects.filter(draft=False).values_list("year", flat=True).distinct("year")
        return context

class MovieDetailView(generic.DetailView):
    """Отдельный фильм"""
    model = Movie

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["last_movies"] = Movie.objects.filter(draft=False).order_by("-id")[:4]
        context["categories"] = Category.objects.all()
        context["genres"] = Genre.objects.all()
        context["years"] = Movie.objects.filter(draft=False).values_list("year", flat=True).distinct("year")
        return context

class ActorDetailView(generic.DetailView):
    """Отдельный фильм"""
    model = Actor

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["last_movies"] = Movie.objects.filter(draft=False).order_by("-id")[:4]
        context["categories"] = Category.objects.all()
        context["genres"] = Genre.objects.all()
        context["years"] = Movie.objects.filter(draft=False).values_list("year", flat=True).distinct("year")
        return context

class FilterMoviesView(generic.ListView):
    """Фильтр фильмов"""
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["last_movies"] = Movie.objects.filter(draft=False).order_by("-id")[:4]
        context["categories"] = Category.objects.all()
        context["genres"] = Genre.objects.all()
        context["years"] = Movie.objects.filter(draft=False).values_list("year", flat=True).distinct("year")
        return context
    
    def get_queryset(self):
        if self.request.GET.getlist("genre") and self.request.GET.getlist("year") and self.request.GET.getlist("category"):
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")) &
                Q(genres__in=self.request.GET.getlist("genre")) &
                Q(category__in=self.request.GET.getlist("category"))
            )
        elif self.request.GET.getlist("genre") and self.request.GET.getlist("category"):
            queryset = Movie.objects.filter(
                Q(genres__in=self.request.GET.getlist("genre")) &
                Q(category__in=self.request.GET.getlist("category"))
            )
        elif self.request.GET.getlist("category") and self.request.GET.getlist("year"):
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")) &
                Q(category__in=self.request.GET.getlist("category"))
            )
        elif self.request.GET.getlist("genre") and self.request.GET.getlist("year"):
            queryset = Movie.objects.filter(
                Q(genres__in=self.request.GET.getlist("genre")) &
                Q(year__in=self.request.GET.getlist("year"))
            )
        else:
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")) |
                Q(genres__in=self.request.GET.getlist("genre")) |
                Q(category__in=self.request.GET.getlist("category"))
            )
        return queryset