release: python manage.py migrate

web: gunicorn movie_web.wsgi --log-file -

worker: python manage.py rqworker default