from django.contrib import admin
from .models import Category, Genre, Movie, Actor, Reviews
# Register your models here.


admin.site.register(Category)
admin.site.register(Genre)
# admin.site.register(Movie)
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_poster', 'display_director', 'display_actor', 'category', 'display_genre', 'draft')
    list_filter = ('category', 'year')

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')

admin.site.register(Reviews)
