# Generated by Django 4.0.4 on 2022-05-22 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_reviews_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reviews',
            name='name',
        ),
    ]
