from asyncio.log import logger
import collections
from urllib import request
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import User

# Create your tests here.

from movie.models import Category, Genre, Movie
from django.urls import reverse

from movie.views import SearchMovieView


class MovieListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_movies = 10
        for movie_num in range(number_of_movies):
            Movie.objects.create(title=f'Terminator {movie_num}')

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
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['movie_list']) == 3)

    def test_lists_all_authors(self):
        resp = self.client.get(reverse('movies')+'?page=4')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['movie_list']) == 1)


class MovieDetailViewTest(TestCase):

    def setUp(self):
        self.movie = Movie.objects.create(title='Terminator', video='https://www.youtube.com/watch?v=k64P4l2Wmeg&t=31s')

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
        Movie.objects.create(title='Terminator')
        Movie.objects.create(title='Avatar')

    def test_details(self):
        url = '{url}?{filter}={value}'.format(
        url=reverse('search'),
        filter='q', value='Ter')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['object_list'], ["<Movie: Terminator>"])


class FilterViewTest(TestCase):

    def setUp(self):
        genre = Genre.objects.create(name='action')
        genre2 = Genre.objects.create(name='fantasy')
        category = Category.objects.create(name='movie')
        category2 = Category.objects.create(name='serial')
        movie1 = Movie.objects.create(title='Terminator', year=1986, category=category)
        movie2 = Movie.objects.create(title='Avatar', year=2009, category=category2)
        movie1.genres.add(genre)
        movie2.genres.add(genre2)
        movie1.save()
        movie2.save()

    def test_details(self):
        url = '{url}?{filter}={value}'.format(
        url=reverse('filter'),
        filter='year', value='1986')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['object_list'], ["<Movie: Terminator>"])
        
        url = '{url}?{filter}={value}&{filter2}={value2}'.format(
        url=reverse('filter'),
        filter='category', value='3',
        filter2="year", value2='2009')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['object_list'], ["<Movie: Avatar>"])
            
        url = '{url}?{filter}={value}&{filter2}={value2}'.format(
        url=reverse('filter'),
        filter='genre', value='2',
        filter2="year", value2='2009')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['object_list'], ["<Movie: Avatar>"])

        url = '{url}?{filter}={value}&{filter2}={value2}'.format(
        url=reverse('filter'),
        filter='genre', value='1',
        filter2="category", value2='2')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['object_list'], ["<Movie: Terminator>"])

        url = '{url}?{filter}={value}&{filter2}={value2}&{filter3}={value3}'.format(
        url=reverse('filter'),
        filter='genre', value='1',
        filter2="category", value2='2',
        filter3="year", value3='1986')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['object_list'], ["<Movie: Terminator>"])

class RegisterViewTest(TestCase):

    def test_register(self):
        resp = self.client.get(reverse('register') )

        self.assertEqual( resp.status_code,200)
        self.assertTemplateUsed(resp, 'account/register.html')
