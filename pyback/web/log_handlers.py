from typing import List


def get_logs_dict() -> List[dict]:
    f = open('logs/log.log')
    # with open('logs/log.log') as f:
    #     logs = [dictify_log(*line.split(" -- ")) for line in f.readlines()]
    # return logs
    return [dictify_log(*line.split(" -- ")) for line in f.readlines()]


def dictify_log(timestamp: str, level: str, message: str) -> dict:
    """
    Utility method for splitting each line in the log into its components
    """
    return {
        'timestamp': timestamp,
        'level': level,
        'message': message
    }
