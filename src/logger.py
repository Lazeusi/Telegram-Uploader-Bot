import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(LOG_DIR, "bot.log")

#Logging settings
logger = logging.getLogger("bot")
logger.setLevel(logging.INFO)

#Log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#File handler
file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
file_handler.setFormatter(formatter)

# Stream handler
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.info("Logger initialized")