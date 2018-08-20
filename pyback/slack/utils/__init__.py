from time import time


def now():
    """
    This has to be pulled out into its own method so a mock can
    be injected for testing purposes
    """
    return int(time())
