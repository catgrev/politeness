from flask import Flask
from celery import Celery
#from flask.ext.cors import CORS, cross-origin

app = Flask(__name__)
#cors = CORS(flask_politeness)
#flask_politeness.config['CORS-HEADERS'] = 'Content-Type'

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)
celery.conf.update(CELERY_ACCEPT_CONTENT = ['pickle'])

@celery.task()
def add_together(a, b):
    return a + b

@app.route('/')
#@cross_origin()
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(threaded=True)
