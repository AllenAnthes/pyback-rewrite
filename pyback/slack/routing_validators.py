from functools import wraps

from flask import request, json, redirect, current_app
from werkzeug.local import LocalProxy

logger = LocalProxy(lambda: current_app.logger)


def validate_request(key_name, valid_key, request_type):
    def validate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if request_type == 'form':
                    data = json.loads(request.form['payload'])
                elif request_type == 'values':
                    data = request.values
                else:
                    data = request.json
                if key_name in data.keys() and data[key_name] != valid_key:
                    return redirect('error.html', code=403)

            except Exception as ex:
                logger.exception('Exception thrown when validating request key', ex)
                return redirect('400.html', code=400)

            return func(*args, **kwargs)

        return wrapper

    return validate


def url_verification_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        data = request.json
        if 'type' in data.keys() and data['type'] == 'url_verification':
            return data['challenge']

        return func(*args, **kwargs)

    return wrapper
