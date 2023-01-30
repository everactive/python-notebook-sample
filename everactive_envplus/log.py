"""Contains logging functionality for the everactive_envplus library."""

import logging
import logging.config
import os


def get_logger() -> logging.Logger:
    """Return a logging.Logger object with a default logging level of INFO.

    Logging level can be set via the LOG_LEVEL environment variable.

    Typical usage example:
        import everactive_envplus.log as logger
        log = logger.get_logger()

        log.info("Log an info message")
        log.error("Log an error message")
    """

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "f": {
                    "format": "[%(levelname)s] %(asctime)s (%(process)d) %(module)s: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            "handlers": {
                "h": {
                    "class": "logging.StreamHandler",
                    "formatter": "f",
                    "level": log_level,
                }
            },
            "loggers": {"default": {"handlers": ["h"], "level": log_level}},
        }
    )

    return logging.getLogger("default")
