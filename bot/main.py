from datetime import datetime
from time import sleep
import redis
from redis.lock import Lock
from celery import Task
from models import Sneaker, Attributes, BoughtSneaker, ScrappingStatus, create_tables, Session, fill_attributes_table, fill_scrapping_status
from helper import diff_more_than_3_hours
from plugins.mobileView import mobileView
from sqlalchemy import select
from core.log import logger
from plugins.mobileHelper import driver

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

            finally:
                if have_lock:
                    lock.release()

        return _caller

    return _dec(function) if function is not None else _dec

# Execute once
# create_tables()
# fill_attributes_table()
# fill_scrapping_status()


class SingleTask(Task):
    @only_one(key="SingleTask", timeout=60 * 30)
    def run(self, **kwargs):
        # Set the scraping date to now and the finishedscrapping to false at first, once we finish we set it to true
        # From the second time and onward we check if the difference between last scrapping and now is more than 3 hours or if finishedscrapping is false, if it's true:
        # We update scraping date to now and we put finishedscrapping to false then we start scrapping
        # once done we put finished scrapping to true and we ignore it for the next 3 hours or so
        with Session as session:
            android = mobileView()
            scrapping_status = session.scalars(select(ScrappingStatus)).first()
            if scrapping_status.finished_scrapping == False or diff_more_than_3_hours(datetime.now(), scrapping_status.last_scrapped):
                android.scrap_sneakers()
                # scrapping_status.last_scrapped = datetime.now()
                # scrapping_status.finished_scrapping = True
                # session.commit()

            driver.quit()

if __name__ == '__main__':
    try:
        from plugins import test
        test.test_scrap_pages(1)
        exit(1)
        with Session as session:
            android = mobileView()
            scrapping_status = session.query(ScrappingStatus).first() 
            if not scrapping_status.finished_scrapping or diff_more_than_3_hours(datetime.now(), scrapping_status.last_scrapped):
                logger.info('started scrapping sneakers.')
                android.scrap_sneakers()
                # scrapping_status.last_scrapped = datetime.now()
                # scrapping_status.finished_scrapping = True
                # session.commit()

                driver.quit()   
    except Exception as e:
        print(e.args[0])
        driver.quit()