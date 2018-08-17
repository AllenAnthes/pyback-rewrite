from flask import jsonify

from pyback import app
from pyback.handlers.handle_code_school import get_logo
from pyback.handlers.message_handlers import delete
from pyback.handlers.slash_command_handlers import get_logs


@app.route('/api/logs/<level>')
def api_logs(level):
    logs = get_logs(level)
    actual_logs = [{'log': log} for log in logs]
    data = jsonify({'data': actual_logs})
    return data


@app.route('/api/delete/<ts>/<channel>')
def delete_message(ts, channel):
    response = delete(ts, channel)
    return jsonify(response)


@app.route('/images/<filename>')
def route_get_logo(filename):
    """
    Fetches stored image.  Used for codeschool icons.
    """
    return get_logo(filename)
