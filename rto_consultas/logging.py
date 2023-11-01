import os
import logging
import logging.config

import inspect
import traceback

LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")

def print_stack():
   frame = inspect.currentframe()
   stack_trace = traceback.format_stack(frame)
   return ''.join(stack_trace)


def configure_logger(log_filename, filename=__name__):
    log_config = {
        "version": 1,
        "formatters": {
            "verbose": {
                "format": "[{levelname}]--[{asctime}] -- [{module}-{lineno}--{funcName}] => {message}",
                "style": "{",
            },
        },
        "handlers": {
            "file": {
                "level": LOG_LEVEL,
                "class": "logging.FileHandler",
                "filename": log_filename,
                "formatter": "verbose",
            },
            "console": {
                "level": LOG_LEVEL,
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["file", "console"],
            "level": LOG_LEVEL,
        },
    }

    logging.config.dictConfig(log_config)

    logger = logging.getLogger(filename)
    return logger


# Usage example in other modules
if __name__ == "__main__":
    logger = configure_logger("/path/to/your/logfile.log")
    logger.debug("This message will be logged to the file and stdout.")
