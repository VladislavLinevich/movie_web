from asgiref.sync import sync_to_async
from movie.models import Movie
from django.db.models import Q


@sync_to_async
def get_search_movies(request):
    return Movie.objects.filter(title__icontains=request.GET.get("q"))


@sync_to_async
def get_filter_movies(request):
    if request.GET.getlist("genre") and request.GET.getlist("year") and request.GET.getlist("category"):
        queryset = Movie.objects.filter(
            Q(year__in=request.GET.getlist("year")) & Q(genres__in=request.GET.getlist("genre")) & Q(category__in=request.GET.getlist("category"))
        ).distinct("title")
    elif request.GET.getlist("genre") and request.GET.getlist("category"):
        queryset = Movie.objects.filter(
            Q(genres__in=request.GET.getlist("genre")) & Q(category__in=request.GET.getlist("category"))
        ).distinct("title")
    elif request.GET.getlist("category") and request.GET.getlist("year"):
        queryset = Movie.objects.filter(
            Q(year__in=request.GET.getlist("year")) & Q(category__in=request.GET.getlist("category"))
        ).distinct("title")
    elif request.GET.getlist("genre") and request.GET.getlist("year"):
        queryset = Movie.objects.filter(
            Q(genres__in=request.GET.getlist("genre")) & Q(year__in=request.GET.getlist("year"))
        ).distinct("title")
    else:
        queryset = Movie.objects.filter(
            Q(year__in=request.GET.getlist("year")) | Q(genres__in=request.GET.getlist("genre")) | Q(category__in=request.GET.getlist("category"))
        ).distinct("title")
    return queryset
