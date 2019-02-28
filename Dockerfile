FROM python:3.5

ENV PYTHONBUFFERED 1

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

# Installing project requirements
RUN pip3 install -r requirements.txt

# Generating env file
ADD .env.example /code/.env

ADD . /code

# Creating database sqlite3 file
RUN touch /code/db/development.sqlite3

# Running migrations then seed the database
RUN python3 manage.py migrate && python3 manage.py seed

EXPOSE 8000

CMD ["gunicorn", "app.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]