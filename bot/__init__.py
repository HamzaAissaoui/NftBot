from celery import Celery
from celery.utils.log import get_task_logger
from bot.main import SingleTask
from bot.config.settings import Settings
from bot.helper import logger

app = Celery('bot', broker=Settings.get_celery_broker())

@app.task
def my_task():
    SingleTask().run()

app.conf.timezone = 'UTC'
app.conf.beat_schedule = {
        "bot-task": {
            "task": "bot.my_task",
            "schedule": 5.0,
        }
    }
