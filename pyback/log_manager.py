import json
import logging.config
import os
import decouple


# https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
def setup_logging(default_level=logging.DEBUG):
    if not os.path.exists('logs'):
        os.mkdir('logs')

    logging_config = decouple.config('LOGGING_CONFIG', default='log_config.json')
    file_path = os.path.join(os.path.dirname(__file__), logging_config)

    if os.path.exists(file_path):
        with open(file_path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
