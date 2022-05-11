from distutils.log import log
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
stream_h = logging.StreamHandler()
formater = logging.Formatter('%(asctime)s - %(message)s')
stream_h.setFormatter(formater)
stream_h.setLevel(logging.INFO)
logger.addHandler(stream_h)

def diff_more_than_3_hours(date_1, date_2, hours_difference=3):
    if (date_1 - timedelta(hours=hours_difference)) >= date_2:
        return True
    return False

