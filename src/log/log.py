import logging
import json

from domain import get_settings

settings = get_settings()


class Formatter(logging.Formatter):
    def format(self, record) -> str:
        log_record = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
        }
        
        if hasattr(record, 'details'):
            log_record.update(record.details)
        return json.dumps(log_record)


class Log(logging.Logger):
    def __init__(self, formatter: Formatter) -> None:
        super().__init__(settings.SERVICE_NAME, level=logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.addHandler(handler)
