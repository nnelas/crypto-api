from flask import Flask
from celery import Celery


app = Flask('crypto')
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0'
)


worker = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
worker.conf.update(app.config)
worker.autodiscover_tasks(["tasks"], related_name="crypto", force=True)
