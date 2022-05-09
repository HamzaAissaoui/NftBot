from celery import Celery
from celery.utils.log import get_task_logger
from bot.controler import SingleTask

app = Celery('bot', broker="amqp://guest:guest@localhost:5672//")
app.conf.timezone = 'UTC'
logger = get_task_logger(__name__)

@app.task
def my_task():
    SingleTask().run()

app.conf.beat_schedule = {
        "bot-task": {
            "task": "bot.my_task",
            "schedule": 30.0,
        }
    }
