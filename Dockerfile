FROM python:3

RUN apt-get update && apt-get -y install cron

COPY . /app
WORKDIR /app
RUN pip install pipenv
RUN pipenv install

RUN pipenv run python src/scheduler.py
CMD cron && tail -f /app/cron.log