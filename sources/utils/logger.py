import logging
import json
from typing import Literal


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "funcName": record.funcName,
            "lineNo": record.lineno,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record, ensure_ascii=False)


class Logger(logging.Logger):
    def __init__(
            self,
            *args,
            format: Literal['json', 'human-readable'] = 'human-readable',
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.setLevel(logging.DEBUG)
        self.handler = logging.StreamHandler()

        if format == 'json':
            self.formatter = JsonFormatter()
        else:
            self.formatter = logging.Formatter(
                fmt="%(asctime)s %(levelname)s %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        self.handler.setFormatter(self.formatter)

        if not self.hasHandlers():
            self.addHandler(self.handler)
        else:
            for h in self.handlers:
                h.setFormatter(self.formatter)
