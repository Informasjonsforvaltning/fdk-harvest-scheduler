# fdk-harvest-scheduler

The fdk-harvest-scheduler creates a cron job  that will send a message to a RabbitMQ every 6th hour.

## Test the job locally

### Requirements
- pipenv

### In your command line
```
% pipenv shell
% pipenv install
% pipenv run python jobs/harvest.py
```

## Test the schedulere locally

### Requirements
- pipenv

### In your command line
```
% pipenv shell
% pipenv install
% pipenv run python src/scheduler.py
```

## Test the scheduler in docker

### Requirements
- docker

### In you command line
```
% docker build . -t eu.gcr.io/fdk-infra/fdk-harvest-scheduler:latest
% docker run eu.gcr.io/fdk-infra/fdk-harvest-scheduler:latest
```

## Test the scheduler in docker-compose

### Requirements
- docker
- docker-compose

### In your command line
```
% docker-compose up  --build
```
