from unicodedata import name
import factory
from movie.models import Actor, Category, Genre, Movie

from faker import Faker

faker = Faker()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: faker.name())


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.LazyAttribute(lambda _: faker.name())


class ActorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Actor

    name = factory.LazyAttribute(lambda _: faker.name())
    age = factory.LazyAttribute(lambda _: faker.pyint(min_value=0, max_value=100))
    description = factory.LazyAttribute(lambda _: faker.text())
    image = factory.LazyAttribute(lambda _: faker.image_url())


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    date_creation = factory.LazyAttribute(lambda _: faker.date_time())
    title = factory.LazyAttribute(lambda _: faker.pystr(max_chars=80))
    tagline = factory.LazyAttribute(lambda _: faker.pystr(max_chars=80))
    description = factory.LazyAttribute(lambda _: faker.text())
    poster = factory.LazyAttribute(lambda _: faker.image_url())
    year = factory.LazyAttribute(lambda _: faker.pyint(min_value=1900, max_value=2021))
    country = factory.LazyAttribute(lambda _: faker.pystr(max_chars=20))

    @factory.post_generation
    def directors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for director in extracted:
                self.directors.add(director)

    @factory.post_generation
    def actors(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for actor in extracted:
                self.actors.add(actor)
    
    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for genre in extracted:
                self.genres.add(genre)
    world_premiere = factory.LazyAttribute(lambda _: faker.date_time())
    budget = factory.LazyAttribute(lambda _: faker.pyint())
    fees_in_usa = factory.LazyAttribute(lambda _: faker.pyint())
    fess_in_world = factory.LazyAttribute(lambda _: faker.pyint())
    category = factory.SubFactory(CategoryFactory)
    video = 'https://www.youtube.com/watch?v=k64P4l2Wmeg&t=31s'
    