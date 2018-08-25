from flask import render_template, current_app
from werkzeug.local import LocalProxy

from pyback.errors import bp

logger = LocalProxy(lambda: current_app.logger)


@bp.app_errorhandler(404)
def page_not_found(error):
    logger.info('404')
    message = 'The requested resource could not be found but may be available again in the future.'
    return render_template('errors/error.html', name='Resource not found', code=404, message=message), 404


@bp.app_errorhandler(403)
def page_forbidden(error):
    message = 'The requested resource requires an authentication.'
    return render_template('errors/error.html', name='Access Denied', code=403, message=message), 403


@bp.app_errorhandler(410)
def page_gone(error):
    message = 'The requested resource is no longer available.'
    return render_template('errors/error.html', name='Resource Not Found', code=410, message=message), 410

# @app.errorhandler(500)
# def internal_server_error(error):
#     return render_template('status/500.html',
#                            event_id=g.sentry_event_id,
#                            public_dsn=sentry.client.get_public_dsn('https')
#                            )
