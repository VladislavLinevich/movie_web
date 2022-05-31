from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from movie_web.settings import dev
from .models import Movie
import datetime

@shared_task(bind=True)
def send_mail_func(self):
    users = get_user_model().objects.all()
    date_from = datetime.datetime.now() - datetime.timedelta(days=1)
    movies = Movie.objects.filter(draft=False, date_creation__gte=date_from)
    mail_subject = "Фильмы, которые были добавлены за последние 24 часа"
    message = ', '.join([movie.title for movie in movies])
    for user in users:
        to_email = user.email
        send_mail(
            subject = mail_subject,
            message=message,
            from_email=dev.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )
    return "Done"