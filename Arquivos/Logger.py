import logging
from sys import platform


def unix_color(value):
    if platform.startswith("win"):
        return ""
    return value


class Colors:
    NONE = unix_color("\x1b[0m")
    BLACK = unix_color("\x1b[30m")
    MAGENTA = unix_color("\x1b[95m")
    BLUE = unix_color("\x1b[94m")
    GREEN = unix_color("\x1b[92m")
    RED = unix_color("\x1b[91m")
    YELLOW = unix_color("\x1b[93m")
    CYAN = unix_color("\x1b[96m")
    WHITE = unix_color("\x1b[97m")


class Logs(Colors):

    FILENAME = "mylogs.log"
    DATE_FORMAT = "%d/%m/%Y %H:%M:%S"

    def __init__(self, filename=FILENAME, datefmt=DATE_FORMAT, logLevel = "info"):
        self.filename = filename
        self.date_format = datefmt
        self.formated = "%(levelname)s:[%(asctime)s]: %(message)s"

        self.logLevel = self.whichLogLevel(logLevel)

        self.levels = {
            "exception": logging.exception,
            "info": logging.info,
            "warning": logging.warning,
            "error": logging.error,
            "debug": logging.debug,
            "critical": logging.critical
        }

    def record(self, msg, *args, exc_info=True, type="exception", colorize=False,**kwargs):
        """
        It takes a message, and a type of message, and logs it to a file
        
        :param msg: The message to log
        :param exc_info: If True, exception information is added to the logging message, defaults to
        True (optional)
        :param type: The type of log you want to record, defaults to exception (optional)
        :param colorize: If True, the log messages will be colored, defaults to False (optional)
        :return: The return value of the method is the return value of the method called.
        """
        for item in self.levels.keys():
            if item == type:
                if not colorize:
                    formated = self.formated
                else:
                    if item == "warning":
                        formated = (
                            f"{self.YELLOW}%(levelname)s:{self.GREEN}[%(asctime)s]"
                            f"{self.NONE}: %(message)s"
                        )
                    elif item == "error" or item == "exception":
                        formated = (
                            f"{self.RED}%(levelname)s:{self.GREEN}[%(asctime)s]"
                            f"{self.NONE}: %(message)s"
                        )
                    else:
                        formated = (
                            f"{self.CYAN}%(levelname)s:{self.GREEN}[%(asctime)s]"
                            f"{self.NONE}: %(message)s"
                        )
                logging.basicConfig(filename=self.filename, format=formated,
                                    datefmt=self.date_format, level=self.logLevel)
                if item == "exception":
                    return self.levels[item](msg, *args, exc_info=exc_info,
                                             **kwargs)
                else:
                    return self.levels[item](msg, *args, **kwargs)
        raise ValueError(
            f'Error implementing the method "{self.record.__name__}" in class Logs.'
        )
    def whichLogLevel(self,logLevel):   
        if logLevel == "warning":
            return logging.WARN
        if logLevel == "error" or logLevel == "exception":
            return logging.ERROR
        if logLevel == "info":
            return logging.INFO
        if logLevel == "debug":
            return logging.DEBUG
        if logLevel == "critical":
            return logging.CRITICAL
        return logging.INFO
            