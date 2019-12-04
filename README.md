# Crypto-API

### Requirements
```
$ brew install redis, pipenv
$ pipenv install
```

### How to run
```
Flask:
$ pipenv run python crypto_flask.py

Redis:
$ redis-server

Celery:
$ pipenv run celery worker -A crypto_celery.worker --loglevel=info -B

Flower: 
$ pipenv run flower -A crypto_celery.worker --port=5555
```

### Notes
```
What is a task queue?
- mechanism to distribute small units of work or tasks that can be 
executed without interfering with the request-response cycle of 
most web-based applications

Flow?
Flask -> Redis -> Celery

Why Celery?
- scalable (allows more workers to be added on-demand to cater to increased 
load or traffic)
- easy to integrate into multiple web frameworks
- in active development

Why "force=True"?
- by default this call is lazy so that the actual auto-discovery won’t happen 
until an application imports the default modules.
- forcing will cause the auto-discovery to happen immediately.
```