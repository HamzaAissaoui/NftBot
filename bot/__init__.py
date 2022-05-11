from celery import Celery
from celery.utils.log import get_task_logger
from main import SingleTask
from config.settings import Settings

app = Celery('bot', broker=Settings.get_celery_broker())
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
