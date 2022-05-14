import logging
from celery.utils.log import get_task_logger
from colorama import Fore, Style
from colorama import init as init_colorama
from uuid import uuid4
from logging import LogRecord
from logging.handlers import RotatingFileHandler
import os

COLORS = {
    "DEBUG": Style.DIM,
    "INFO": Fore.WHITE,
    "WARNING": Fore.YELLOW,
    "ERROR": Fore.RED,
    "CRITICAL": Fore.MAGENTA,
}


class ColoredFormatter(logging.Formatter):
    def __init__(self, *, fmt, datefmt=None):
        logging.Formatter.__init__(self, fmt=fmt, datefmt=datefmt)

    def format(self, record):
        msg = super().format(record)
        levelname = record.levelname
        if hasattr(record, "color"):
            return f"{record.color}{msg}{Style.RESET_ALL}"
        if levelname in COLORS:
            return f"{COLORS[levelname]}{msg}{Style.RESET_ALL}"
        return msg

def create_log_file_handler(filename):
    file_handler = RotatingFileHandler(
        filename,
        mode="a",
        backupCount=10,
        maxBytes=15 * 1000000,
        encoding="utf-8",
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(levelname)8s | %(message)s (%(filename)s:%(lineno)d)",
            datefmt=r"[%m/%d %H:%M:%S]",
        )
    )
    return file_handler


def configure_logger(filename):
    global g_session_id
    global g_log_file_name
    global g_logs_dir
    global g_file_handler
    global g_log_file_updated

    console_level = logging.INFO

    g_session_id = uuid4()
    g_logs_dir = "logs"
    if filename:
        g_log_file_name = f"{filename}.log"
        g_log_file_updated = True
    else:
        g_log_file_name = f"{g_session_id}.log"
        g_log_file_updated = False

    init_colorama()

    # Root logger
    root_logger = get_task_logger(__name__)
    # root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Console logger (limited but colored log)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(
        ColoredFormatter(
            fmt="%(asctime)s %(levelname)8s | %(message)s", datefmt="[%m/%d %H:%M:%S]"
        )
    )

    root_logger.addHandler(console_handler)

    # File logger (full raw log)
    if not os.path.exists(g_logs_dir):
        os.makedirs(g_logs_dir)
    g_file_handler = create_log_file_handler(f"{g_logs_dir}/{g_log_file_name}")
    root_logger.addHandler(g_file_handler)

    init_logger = logging.getLogger(__name__)
    init_logger.debug(f"Initial log file: {g_logs_dir}/{g_log_file_name}")
    return root_logger


logger = configure_logger('logs')