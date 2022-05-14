from datetime import datetime
import imp
from time import sleep
import redis
from redis.lock import Lock
from celery import Task
from bot.models import Sneaker, Attributes, BoughtSneaker, ScrappingStatus, create_tables, db, fill_attributes_table, fill_scrapping_status
from bot.helper import  diff_more_than_3_hours
from bot.plugins.mobileView import mobileView
from sqlalchemy import select
from bot.helper import logger

android = mobileView()
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
                is_locked = Lock(REDIS_CLIENT, key).locked()
                if have_lock:
                    run_func(*args, **kwargs)
                else:
                    logger.info('scrapping running, this might take a while..')
                    
            finally:
                if have_lock:
                    lock.release()

        return _caller

    return _dec(function) if function is not None else _dec

# Execute once
# create_tables()
# fill_attributes_table()
#fill_scrapping_status()


class SingleTask(Task):
    @only_one(key="SingleTask", timeout=60 * 30)
    def run(self, **kwargs):
        #Set the scraping date to now and the finishedscrapping to false at first, once we finish we set it to true
        #From the second time and onward we check if the difference between last scrapping and now is more than 3 hours or if finishedscrapping is false, if it's true:
        #We update scraping date to now and we put finishedscrapping to false then we start scrapping
        #once done we put finished scrapping to true and we ignore it for the next 3 hours or so
        with db as session:
            scrapping_status = session.scalars(select(ScrappingStatus)).first()
            if scrapping_status.finished_scrapping == False or diff_more_than_3_hours(datetime.now(), scrapping_status.last_scrapped): 
                android.scrap_sneakers()
                # scrapping_status.last_scrapped = datetime.now()
                # scrapping_status.finished_scrapping = True
                # session.commit()
        

