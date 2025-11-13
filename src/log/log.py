import logging
from logging import LogRecord
import json
from datetime import datetime, timezone

from domain import get_settings

settings = get_settings()


class Formatter(logging.Formatter):
    def format(self, record: LogRecord) -> str:
        timestamp = datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat()

        log_record = {
            'timestamp': timestamp,
            'level': record.levelname,
            'logger': record.name,
            'path': record.pathname,
            'message': record.getMessage()
        }

        if hasattr(record, 'details'):
            for key, value in record.details.items():
                record.details[key] = str(value)
            log_record.update(record.details)

        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)

        if record.stack_info:
            log_record['stack_trace'] = self.formatStack(record.stack_info)
            
        return json.dumps(log_record)


class Log(logging.Logger):
    def __init__(self, formatter: Formatter) -> None:
        super().__init__(settings.SERVICE_NAME, level=logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        self.addHandler(handler)
