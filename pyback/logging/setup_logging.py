import logging
import sys
import os

fmt = '{asctime} -- {levelname} -- {module}.{funcName} : {lineno}, {message}', None, "{"


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super().formatException(exc_info)
        return repr(result)

    def format(self, record):
        s = super().format(record)
        if record.exc_text:
            s = s.replace('\n', ' ') + '|'
        return s


class CustomFileHandler(logging.FileHandler):
    def __init__(self):
        super().__init__('logs/log.log', encoding='utf8')
        self.formatter = OneLineExceptionFormatter(*fmt)


class CustomConsoleHandler(logging.StreamHandler):
    def __init__(self):
        super().__init__(sys.stdout)
        self.formatter = logging.Formatter(*fmt)


if not os.path.exists('logs'):
    os.mkdir('logs')

console_handler = CustomConsoleHandler()
file_handler = CustomFileHandler()
root = logging.getLogger()
root.addHandler(console_handler)
root.addHandler(file_handler)

# pyback_logger = logging.getLogger('pyback')
# slack_logger = logging.getLogger('flask_slack_client')
# airtable_logger = logging.getLogger('flask_airtable_client')

loggers = [logging.getLogger(name) for name in ['pyback', 'slack_client', 'airtable_client']]
for logger in loggers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.DEBUG)

logging.getLogger('socketio').setLevel(logging.ERROR)
logging.getLogger('engineio').setLevel(logging.ERROR)
