import redis
import time
from celery import Task
from bot.models import Sneaker, Attributes, BoughtSneaker, create_tables, db
REDIS_CLIENT = redis.Redis()

def only_one(function=None, key="", timeout=None):
    """Enforce only one celery task at a time."""

    def _dec(run_func):
        """Decorator."""

        def _caller(*args, **kwargs):
            """Caller."""
            have_lock = False
            lock = REDIS_CLIENT.lock(key, timeout=timeout)
            try:
                have_lock = lock.acquire(blocking=False)
                if have_lock:
                    run_func(*args, **kwargs)
                else:
                    print('locked')
            finally:
                if have_lock:
                    lock.release()

        return _caller

    return _dec(function) if function is not None else _dec

create_tables()

class SingleTask(Task):
    @only_one(key="SingleTask", timeout=60*30)
    def run(self, **kwargs):
        print("Running Task!")
        time.sleep(5)

