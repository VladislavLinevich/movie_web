from asyncio.log import logger
import collections
from urllib import request
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User

# Create your tests here.

from movie.models import Category, Genre, Movie
from django.urls import reverse
from movie.tests.factories import GenreFactory, MovieFactory

from movie.views import SearchMovieView


class MovieListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_movies = 10
        for movie_num in range(number_of_movies):
            MovieFactory.create()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('movies'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('movies'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'movie/movie_list.html')

    def test_pagination_is_three(self):
        resp = self.client.get(reverse('movies'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['movie_list']) == 3)

    def test_lists_all_authors(self):
        resp = self.client.get(reverse('movies') + '?page=4')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['movie_list']) == 1)


class MovieDetailViewTest(TestCase):

    def setUp(self):
        self.movie = MovieFactory()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(f'/movie/{self.movie.pk}/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('movie-detail', kwargs={'pk': self.movie.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('movie-detail', kwargs={'pk': self.movie.pk}))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'movie/movie_detail.html')


class SearchViewTest(TestCase):

    def setUp(self):
        MovieFactory.create(title='Terminator')
        MovieFactory.create(title='Avatar')

    def test_details(self):
        url = '{url}?{filter}={value}'.format(url=reverse('search'), filter='q', value='Ter')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['object_list'], ["<Movie: Terminator>"])


class FilterViewTest(TestCase):

    def setUp(self):
        self.genre = GenreFactory()
        self.genre2 = GenreFactory()
        self.movie1 = MovieFactory(genres=(self.genre, ))
        self.movie2 = MovieFactory(genres=(self.genre2, ))

    def test_details(self):
        url = '{url}?{filter}={value}'.format(url=reverse('filter'), filter='year', value=f'{self.movie1.year}')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['object_list'], [f"<Movie: {self.movie1.title}>"])

        url = '{url}?{filter}={value}&{filter2}={value2}'.format(url=reverse('filter'), filter='category', value=f'{self.movie2.category.id}', filter2="year", value2=f'{self.movie2.year}')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['object_list'], [f"<Movie: {self.movie2.title}>"])

        url = '{url}?{filter}={value}&{filter2}={value2}'.format(url=reverse('filter'), filter='genre', value=f'{self.genre2.id}', filter2="year", value2=f'{self.movie2.year}')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['object_list'], [f"<Movie: {self.movie2.title}>"])

        url = '{url}?{filter}={value}&{filter2}={value2}'.format(url=reverse('filter'), filter='genre', value=f'{self.genre.id}', filter2="category", value2=f'{self.movie1.category.id}')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['object_list'], [f"<Movie: {self.movie1.title}>"])

        url = '{url}?{filter}={value}&{filter2}={value2}&{filter3}={value3}'.format(url=reverse('filter'), filter='genre', value=f'{self.genre.id}', filter2="category", value2=f'{self.movie1.category.id}', filter3="year", value3=f'{self.movie1.year}')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['object_list'], [f"<Movie: {self.movie1.title}>"])


class RegisterViewTest(TestCase):

    def test_register(self):
        resp = self.client.get(reverse('register'))

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'account/register.html')
