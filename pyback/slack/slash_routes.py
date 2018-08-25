from flask import request, current_app, make_response
from werkzeug.local import LocalProxy

from pyback.slack import bp
from pyback.slack.routing_validators import validate_request
from pyback.slack.slash_handlers import slash_here

logger = LocalProxy(lambda: current_app.logger)
token = LocalProxy(lambda: current_app.config['VERIFICATION_TOKEN'])


@bp.route('/here', methods=['POST'])
@validate_request('token', token, 'values')
def here():
    req = request.values
    return slash_here(req['channel_id'], req['text'], req['user_id'])


@bp.route('/get_logs', methods=['POST'])
@validate_request('token', token, 'values')
def get_logs():
    req = request.values
    logger.debug(f'Log request received: {req}')
    return make_response(f'{request.host_url}admin/logs', 200)
