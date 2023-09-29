import logging
import logging.config


def configure_logger(log_filename):
    log_config = {
        "version": 1,
        "formatters": {
            "verbose": {
                "format": "[{levelname}]--[{asctime}] => {message}",
                "style": "{",
            },
        },
        "handlers": {
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": log_filename,
                "formatter": "verbose",
            },
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["file", "console"],
            "level": "DEBUG",
        },
    }

    logging.config.dictConfig(log_config)

    logger = logging.getLogger(__name__)
    return logger


# Usage example in other modules
if __name__ == "__main__":
    logger = configure_logger("/path/to/your/logfile.log")
    logger.debug("This message will be logged to the file and stdout.")
