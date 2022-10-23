from enum import Enum


class LogType(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

    def get_type(self) -> str:
        log_type = ""
        if self == self.DEBUG:
            log_type = "DEBUG"
        if self == self.INFO:
            log_type = "INFO"
        elif self == self.WARNING:
            log_type = "WARNING"
        elif self == self.ERROR:
            log_type = "ERROR"
        elif self == self.CRITICAL:
            log_type = "CRITICAL"
        return log_type

    def get_color_type(self) -> str:
        log_color_type = ""
        if self == self.INFO:
            log_color_type = "\033[34m"
        elif self == self.WARNING:
            log_color_type = "\033[33m"
        elif self == self.ERROR or self == self.CRITICAL:
            log_color_type = "\033[31m"
        return log_color_type
