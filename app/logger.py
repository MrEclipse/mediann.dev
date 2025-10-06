import logging
from logging.handlers import RotatingFileHandler

"""Логгер с файлом и консолью, ротация по размеру"""

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler("app.log", maxBytes=5_000_000, backupCount=3)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

console = logging.StreamHandler()
console.setFormatter(formatter)
logger.addHandler(console)
