from multiprocessing import context
from pyexpat import model
from django.shortcuts import render
from django.views.generic.base import View

from movie.forms import UserRegistrationForm
from .models import Category, Movie, Actor, Genre
from django.views import generic
from django.db.models import Q

class CustomMixin(object):
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["last_movies"] = Movie.objects.filter(draft=False).order_by("-id")[:4]
        context["categories"] = Category.objects.all()
        context["genres"] = Genre.objects.all()
        context["years"] = Movie.objects.filter(draft=False).values_list("year", flat=True).distinct("year")
        return context

class MovieListView(CustomMixin, generic.ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 3

class MovieDetailView(CustomMixin, generic.DetailView):
    """Отдельный фильм"""
    model = Movie

class ActorDetailView(CustomMixin, generic.DetailView):
    """Отдельный фильм"""
    model = Actor

class FilterMoviesView(generic.ListView):
    """Фильтр фильмов"""
    paginate_by = 3

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["last_movies"] = Movie.objects.filter(draft=False).order_by("-id")[:4]
        context["categories"] = Category.objects.all()
        context["genres"] = Genre.objects.all()
        context["years"] = Movie.objects.filter(draft=False).values_list("year", flat=True).distinct("year")
        context["pagi_year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["pagi_category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
        context["pagi_genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        return context
    
    def get_queryset(self):
        if self.request.GET.getlist("genre") and self.request.GET.getlist("year") and self.request.GET.getlist("category"):
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")) &
                Q(genres__in=self.request.GET.getlist("genre")) &
                Q(category__in=self.request.GET.getlist("category"))
            ).distinct("title")
        elif self.request.GET.getlist("genre") and self.request.GET.getlist("category"):
            queryset = Movie.objects.filter(
                Q(genres__in=self.request.GET.getlist("genre")) &
                Q(category__in=self.request.GET.getlist("category"))
            ).distinct("title")
        elif self.request.GET.getlist("category") and self.request.GET.getlist("year"):
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")) &
                Q(category__in=self.request.GET.getlist("category"))
            ).distinct("title")
        elif self.request.GET.getlist("genre") and self.request.GET.getlist("year"):
            queryset = Movie.objects.filter(
                Q(genres__in=self.request.GET.getlist("genre")) &
                Q(year__in=self.request.GET.getlist("year"))
            ).distinct("title")
        else:
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")) |
                Q(genres__in=self.request.GET.getlist("genre")) |
                Q(category__in=self.request.GET.getlist("category"))
            ).distinct("title")
        return queryset

class SearchMovieView(generic.ListView):
    """Поиск фильмов"""
    paginate_by = 3

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["last_movies"] = Movie.objects.filter(draft=False).order_by("-id")[:4]
        context["categories"] = Category.objects.all()
        context["genres"] = Genre.objects.all()
        context["years"] = Movie.objects.filter(draft=False).values_list("year", flat=True).distinct("year")
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})