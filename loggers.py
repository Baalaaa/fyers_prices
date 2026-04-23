import os
import logging
import colorlog

from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


# --- LOG File &  LOG Dir ---
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR,f'app_{datetime.today().date().strftime("%Y-%m-%d")}.log')


# --- Logger LEVEL ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# --- Handler ---
handler = TimedRotatingFileHandler(
    filename=LOG_FILE,
    when='midnight',
    interval=1,
    backupCount=6,
)

# --- Formatter ---
formatter = logging.Formatter(
    '%(asctime)s | %(levelname)-6s | %(name)s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s'
)

# ---- Adding Format & Handler ----
handler.setFormatter(formatter)
logger.addHandler(handler)


# ---- Adding Format & Handler ----
console_log = colorlog.StreamHandler()
console_log.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s'
    , datefmt='%Y-%m-%d %H:%M:%S'))
logger.addHandler(console_log)