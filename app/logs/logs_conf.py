import logging
from logging.handlers import SysLogHandler
from coloredlogs import ColoredFormatter
from app.config import settings


"""___APPLICATION LOGS CONFIGURATIONS__
"""


def log_levels() -> logging.Logger:
    logger = logging.getLogger(settings.analyzer)
    logger.setLevel(logging.DEBUG)

    handler = SysLogHandler(
        address=(settings.papertrail_host, settings.papertrail_port)
    )
    handler.setLevel(logging.DEBUG)

    formatter = ColoredFormatter(
        f"{settings.analyzer} %(asctime)s %(levelname)s %(pathname)s:%(lineno)d %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
