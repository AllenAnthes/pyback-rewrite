from time import time
from typing import NamedTuple

ResponseContainer = NamedTuple('ResponseContainer', [('route', str), ('method', str), ('payload', dict)])


def now():
    """
    This has to be pulled out into its own method so a mock can
    be injected for testing purposes
    """
    return int(time())
