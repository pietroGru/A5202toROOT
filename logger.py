#################################################################################################
# @info Logging library with custom codes and colors                                            #
# @date 23/07/05                                                                                #
#                                                                                               #
# This library provides a custom logger class, with standard logging levels and two more        #
# TRACE and VERBOSE levels used for very detailed debugging                                     #
#################################################################################################
import logging as loglib
import time

TRACE = 5
VERBOSE = 15

# Subclass the logging.Logger to add custom log methods
class CustomLogger(loglib.Logger):
    """
    Subclass the logging.Logger to add custom log methods
    
    Parameters
    ----------
        name (str) : name of the logger
        level (int) : logging level
    
    Returns
    -------
        None    
    """
    
    TRACE = 5
    VERBOSE = 15
    # Define the corresponding log level names
    loglib.addLevelName(TRACE, "TRACE")
    loglib.addLevelName(VERBOSE, "VERBOSE")

    bashColors = {'grey' : "\x1b[38;20m", 'yellow' : "\x1b[33;20m", 'red' : "\x1b[31;20m", 'bold_red' : "\x1b[31;1m", 'green' : "\x1b[32;1m"}
    reset = "\x1b[0m"
    
    def colormsg(self, color: str, msg: str):
        """
        Print colored message to the console
        
        Parameters
        ----------
            color (str) : color to use among the following: grey, yellow, red, bold_red, green
            msg (str) : message to print
        
        Returns
        -------
            None
        """
        
        msgClr = self.bashColors[color] +  msg + self.reset
        print(msgClr)
    
    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.TRACE):
            self._log(self.TRACE, msg, args, **kwargs)

    def verbose(self, msg, *args, **kwargs):
        if self.isEnabledFor(self.VERBOSE):
            self._log(self.VERBOSE, msg, args, **kwargs)
    
    def status(self, message):
        #return
        green = "\x1b[32;1m"
        reset = "\x1b[0m"
        header = f"[{time.strftime('%H:%M:%S')}] {green}STATUS{reset} - {message}"
        print(header, end="\r", flush=True)
        
    def statusRed(self, message):
        #return
        bold_red = "\x1b[31;1m"
        reset = "\x1b[0m"
        header = f"[{time.strftime('%H:%M:%S')}] {bold_red}STATUS{reset} - {message}"
        print(header, end="\r", flush=True)

# Custom formatter for the logger
class CustomFormatter(loglib.Formatter):
    bold_red = "\x1b[31;1m"
    green = "\x1b[32;1m"
    grey = "\x1b[38;20m"
    red = "\x1b[31;20m"
    yellow = "\x1b[33;20m"
    reset = "\x1b[0m"
    time = "[%(asctime)s]"
    format = " %(levelname)s "
    message = "- %(message)s"
    FORMATS = {
        TRACE: time + red + format + reset + message,
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

# Create a custom logger with the given name and level
def create_logger(name, level=loglib.INFO):
    """
    Create a custom logger with the given name and level
    
    Parameters
    ----------
        name (str) : name of the logger
    
    Returns
    -------
        logger (CustomLogger) : logger object
    """
    
    logger = CustomLogger(name)
    logger.setLevel(level)

    ch = loglib.StreamHandler()
    ch.setLevel(5)                              # Default StreamHandler level set to capture up to TRACE
    ch.setFormatter(CustomFormatter())
    
    logger.addHandler(ch)
    return logger