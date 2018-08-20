def dictify_log(timestamp, level, message):
    return {
        'timestamp': timestamp,
        'level': level,
        'message': message
    }
