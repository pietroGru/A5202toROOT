import logging as loglib

# Configure logger
class CustomFormatter(loglib.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    time = "[%(asctime)s]"
    format = " %(levelname)s "
    message = "- %(message)s"
    FORMATS = {
        loglib.DEBUG: time + grey + format + reset + message,
        loglib.INFO: time + grey + format + reset + message,
        loglib.WARNING: time + yellow + format + reset + message,
        loglib.ERROR: time + red + format + reset + message,
        loglib.CRITICAL: time + bold_red + format + reset + message
    }
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = loglib.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)
# create logger with 'spam_application'
logging = loglib.getLogger("rootConverter")
logging.setLevel(loglib.INFO)
# create console handler with a higher log level
ch = loglib.StreamHandler()
ch.setLevel(loglib.DEBUG)
ch.setFormatter(CustomFormatter())
logging.addHandler(ch)