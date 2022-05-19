from django.urls import path

from . import views

urlpatterns = [
    path('', views.MovieListView.as_view(), name='movies'),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path('movie/<int:pk>/', views.MovieDetailView.as_view(), name='movie-detail'),
    path('actor/<int:pk>/', views.ActorDetailView.as_view(), name='actor-detail'),
]