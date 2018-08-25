from threading import Thread

from flask import current_app, request, make_response, json
from werkzeug.local import LocalProxy

from pyback.slack import bp
from pyback.slack.all_events_router import route_request
from pyback.slack.routing_validators import url_verification_check, validate_request

logger = LocalProxy(lambda: current_app.logger)
token = LocalProxy(lambda: current_app.config['VERIFICATION_TOKEN'])


@bp.route('/slack_event', methods=['POST'])
@url_verification_check
@validate_request('token', token, 'json')
def slack_event():
    """
    Any event based request will get routed here.
    Decorates first make sure it's a verified route and this isn't a challenge event
    """
    request_json = request.json
    logger.debug(f'Slack event received: {json.dumps(request_json)}')

    Thread(target=route_request, kwargs={'event': request_json['event']}).start()

    return make_response('', 200)


@bp.route("/user_interaction", methods=['POST'])
@validate_request('token', token, 'form')
def slack_interaction():
    event = json.loads(request.form['payload'])
    logger.debug(f"Interaction received: {event}")
    Thread(target=route_request, kwargs={'event': event}).start()
    return make_response('', 200)


@bp.route('/mentor_request', methods=['POST'])
def mentor_request():
    event = request.get_json()
    logger.debug(f'Mentor request event received: {event}')
    Thread(target=route_request, kwargs={'event': event}).start()
    return make_response('', 200)