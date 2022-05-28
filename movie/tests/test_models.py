from django.test import TestCase
from movie.models import Category, Movie


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='Боевик')

    def test_str(self):
        category = Category.objects.get(id=1)
        expected_str = f'{category.name}'
        self.assertEquals(expected_str, str(category))


class MovieModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Movie.objects.create(title='Terminator')

    def test_str(self):
        movie = Movie.objects.get(id=1)
        expected_str = f'{movie.title}'
        self.assertEquals(expected_str, str(movie))
