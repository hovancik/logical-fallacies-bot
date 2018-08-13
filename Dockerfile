from python:3.5.3

RUN mkdir /bot
WORKDIR /bot

ADD Pipfile Pipfile.lock /bot/

RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --deploy --system

ADD . /bot
