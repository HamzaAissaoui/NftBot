import redis
from redis.lock import Lock
from celery import Task
from models import Attributes, create_tables, Session, fill_attributes_table, fill_scrapping_status, Sneaker
from helper import checkScrappingStatus, updateScrappingStatus
from plugins.mobileView import mobileView
from core.log import logger
from plugins.mobileHelper import driver
from sqlalchemy import and_
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
        finishedScrapping, threeHoursSinceLastScrap = checkScrappingStatus()
        if not finishedScrapping or threeHoursSinceLastScrap:
            logger.info('started scrapping sneakers.')
            mobileView.scrap_sneakers(startFromPage=20, endAtPage=30)
            updateScrappingStatus()
        driver.quit()


if __name__ == '__main__':
    finishedScrapping, threeHoursSinceLastScrap = checkScrappingStatus()
    if not finishedScrapping or threeHoursSinceLastScrap:
        logger.info('started scrapping sneakers.')
        mobileView.scrap_sneakers(startFromPage=10, endAtPage=30)
        updateScrappingStatus()
    driver.quit()
