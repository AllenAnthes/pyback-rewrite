import logging
from threading import Thread

from flask import request, make_response, json

from pyback import app
from pyback.handlers.slash_command_handlers import can_view_logs, get_temporary_url, handle_log_view
from pyback.utils.routing_validators import validate_request, url_verification_check
from .router import route_request

logger = app.logger


@app.route('/slack_event', methods=['POST'])
@url_verification_check
@validate_request('token', app.config['VERIFICATION_TOKEN'], 'json')
def route_slack_event():
    """
    Any event based response will get routed here.
    Decorates first make sure it's a verified route and this isn't a challenge event
    """
    request_json = request.json
    logger.debug(f'Slack event received: {json.dumps(request_json)}')

    Thread(target=route_request, kwargs={'event': request_json['event']}).start()

    return make_response('', 200)


@app.route("/user_interaction", methods=['POST'])
@validate_request('token', app.config['VERIFICATION_TOKEN'], 'form')
def route_slack_interaction():
    event = json.loads(request.form['payload'])
    logger.info(f"Interaction received: {event}")
    Thread(target=route_request, kwargs={'event': event}).start()
    return make_response('', 200)


@app.route('/mentor_request', methods=['POST'])
def route_mentor_request():
    event = request.get_json()
    logger.info(f'Mentor request event received: {event}')
    Thread(target=route_request, kwargs={'event': event}).start()
    return make_response('', 200)


@app.route('/get_logs', methods=['POST'])
@validate_request('token', app.config['VERIFICATION_TOKEN'], 'values')
def route_logs():
    req = request.values
    logger.info(f'Log request received: {req}')

    if not can_view_logs(req['user_id']):
        logger.info(f"{req['user_name']} attempted to view logs and was denied")
        return make_response("You are not authorized to do that.", 200)

    url = get_temporary_url(req['user_id'], req['text'])
    logger.info(f"Created log URL for {req['user_name']} : {url.url}")
    return make_response(f'{request.host_url}logs/{url.url}', 200)


@app.route("/logs/<variable>")
def show_logs(variable):
    """
    Routes user to log
    :param variable:  Randomly generated string
    """
    return handle_log_view(variable)
