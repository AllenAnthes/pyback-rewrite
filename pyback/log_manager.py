import json
import logging.config
from os import path
import decouple

logger = logging.getLogger(__name__)


# https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
def setup_logging(default_level=logging.INFO):

    logging_config = decouple.config('LOGGING_CONFIG', default='log_config.json')
    file_path = path.join(path.dirname(__file__), logging_config)

    if path.exists(file_path):
        with open(file_path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)

    else:
        logging.basicConfig(level=default_level)
        logger.warning('Warning, verify there is no desired config file')
