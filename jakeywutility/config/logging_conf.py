# __author__ = 'jakey'

import os
from datetime import date


def logging_conf_dict(path):
    sc_logging_conf = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(levelname)s %(asctime)s %(pathname)s %(lineno)d %(message)s",
            },
            "info": {
                "format": "%(levelname)s %(asctime)s %(filename)s %(lineno)d %(message)s",
            },
            "error": {
                "format": "%(levelname)s %(asctime)s %(filename)s %(lineno)d %(message)s",
            }
        },

        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "console",
                "stream": "ext://sys.stdout"
            },

            "info_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "info",
                "filename": os.path.join(path, ("info-" + date.today().isoformat() + ".log")),
                "maxBytes": 1024*5,
                "backupCount": 5,
                "encoding": "utf8"
            },

            "error_file_handler": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "error",
                "filename": os.path.join(path, ("errors-" + date.today().isoformat() + ".log")),
                "maxBytes": 1024*5,
                "backupCount": 5,
                "encoding": "utf8"
            }
        },
        'loggers': {
            "console": {
                "level": "DEBUG",
                "handlers": ["console"]
            },

            "root": {
                "level": "DEBUG",
                "handlers": ["console", "info_file_handler", "error_file_handler"]
            }
        }
    }
    return sc_logging_conf
