FROM python:3.11

RUN apt-get update && apt-get -y install cron

COPY . /app
WORKDIR /app
RUN pip install poetry==1.4.2
RUN poetry install
RUN poetry self add poetry-dotenv-plugin
RUN touch /app/jobs/cron.log

RUN poetry run python -u src/scheduler.py

## Environment variables does NOT get passed to cron,
## so they are invisible to the python script when run in cron.
## Therefore we need to write them to a file:
CMD printenv >> .env && cron && tail -F /app/jobs/cron.log
