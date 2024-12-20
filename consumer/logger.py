import logging.config
from contextvars import ContextVar
from typing import Any

import yaml

with open('config/logging.conf.yml', 'r') as f:
    LOGGING_CONFIG: Any = yaml.full_load(f)


class ConsoleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        correlation_id = correlation_id_context.get(None)

        if correlation_id is not None:
            return '[%s] %s' % (correlation_id, super().format(record))

        return super().format(record)


correlation_id_context: ContextVar[str] = ContextVar('correlation_id')

logger = logging.getLogger('consumer_logger')
