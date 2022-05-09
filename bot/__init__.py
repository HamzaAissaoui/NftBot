from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from celery import Celery
from celery.utils.log import get_task_logger
from bot.controler import SingleTask

'''Comments before every execution'''
@event.listens_for(Engine, "before_cursor_execute")
def comment_sql_calls(conn, cursor, statement, parameters,
                                    context, executemany):
    print('executing: ' + statement + ' with parameters: ' + str(parameters))

'''Creating an engine'''
engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/postgres", echo=False, future=True)

db = Session(engine)
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
