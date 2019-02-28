FROM python:3.5

ENV PYTHONBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

RUN pip3 install -r requirements.txt

ADD .env.example /code/.env

ENV JWT_SECRET_KEY secret

ADD . /code

RUN touch /code/db/development.sqlite3

RUN python3 manage.py migrate

RUN python3 manage.py seed

EXPOSE 8000

CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]