from datetime import datetime
from DataClasses.log_type import LogType


class LogService:
    @staticmethod
    def log(message: str,
            log_type: LogType = LogType.DEBUG):

        log_message = f"{log_type.get_color_type()}" \
                      f"{datetime.now():%d.%m.%Y %H:%M:%S} " \
                      f"[{log_type.get_type()}]: " \
                      f"{message}"
        print(log_message)
