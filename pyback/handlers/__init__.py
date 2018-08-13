import logging

logger = logging.getLogger(__name__)


def default_handler(**event):
    logger.warning(f'Event passed to the default handler: {event}', )
