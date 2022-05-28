import asyncio
from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.contrib import messages
from movie.async_requests import get_filter_movies, get_search_movies
from django.contrib.auth.mixins import LoginRequiredMixin
from movie.forms import ReviewForm, UserRegistrationForm
from .models import Category, Movie, Actor, Genre
from django.views import generic
from django.db.models import Q
import logging
logger = logging.getLogger(__name__)


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
    """Отдельный актер"""
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
        coroutine = get_filter_movies(self.request)
        return asyncio.run(coroutine)


class SearchMovieView(generic.ListView):
    """Поиск фильмов"""
    paginate_by = 3

    def get_queryset(self):
        coroutine = get_search_movies(self.request)
        return asyncio.run(coroutine)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["last_movies"] = Movie.objects.filter(draft=False).order_by("-id")[:4]
        context["categories"] = Category.objects.all()
        context["genres"] = Genre.objects.all()
        context["years"] = Movie.objects.filter(draft=False).values_list("year", flat=True).distinct("year")
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


class RegisterView(View):
    """Регистрация"""
    def get(self, request):
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
        return render(request, 'account/register.html', {'user_form': user_form})


class AddReview(View):
    """Добавление отзыва"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if request.user.is_anonymous:
            logger.info('User cant sent review')
            messages.warning(request, "Вы должны войти в аккаунт!")
            return redirect('/accounts/login/?next=' + movie.get_absolute_url())
        if form.is_valid():
            form = form.save(commit=False)
            form.movie = movie
            form.author = request.user
            form.save()
            messages.success(request, "Отзыв оставлен успешно!")
            logger.info(f'{request.user} sent review for {movie}')
        return redirect(movie.get_absolute_url())
