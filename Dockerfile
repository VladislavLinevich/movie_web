# pull official base image
FROM python:3.9-alpine

# set work directory
WORKDIR /movie_web

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /movie_web/requirements.txt
RUN pip install -r /movie_web/requirements.txt

# copy project
COPY . .
