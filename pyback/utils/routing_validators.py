from functools import wraps

from flask import request, json, redirect


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
                    return redirect('HTTP403.html', code=403)

            except Exception as e:
                return redirect('HTTP400.html', code=400)

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
