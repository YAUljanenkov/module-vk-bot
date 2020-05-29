"""
This file includes special classes to make colored output of logs in Console.
This code was taken from StackOverFlow (author - airmind).
"""
import logging
from logging.handlers import TimedRotatingFileHandler

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

LOG_FILE = "bot.log"

RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}


def get_logger(logger_name):
    logging.setLoggerClass(ColoredLogger)
    logger = logging.getLogger(logger_name)
    logger.propagate = False
    return logger


def formatter_message(message, use_color=True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


# Custom logger class with multiple destinations
class ColoredLogger(logging.Logger):
    FORMAT = "%(asctime)s — [%(name)s] — %(levelname)s — %(message)s"
    COLOR_FORMAT = formatter_message(FORMAT, True)
    FILE_FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

    def __init__(self, name):
        logging.Logger.__init__(self, name, logging.DEBUG)
        color_formatter = ColoredFormatter(self.COLOR_FORMAT)
        console = logging.StreamHandler()
        file = TimedRotatingFileHandler(LOG_FILE, when='midnight')
        console.setFormatter(color_formatter)
        file.setFormatter(self.FILE_FORMATTER)
        self.addHandler(console)
        self.addHandler(file)
        return


