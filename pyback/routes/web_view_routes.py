from flask import render_template, redirect, url_for, request, flash, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_required

from pyback import app
from pyback.handlers.handle_code_school import handle_submission, get_logo
from pyback.handlers.message_handlers import get_messages, delete
from pyback.handlers.slash_command_handlers import get_logs, verify_user
from pyback.utils.forms import CodeSchoolForm

logger = app.logger

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


@limiter.request_filter
def ip_whitelist():
    return request.remote_addr in ["127.0.0.1", "localhost"]


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route("/logs/<variable>")
def show_logs(variable):
    """
    Routes user to log
    :param variable:  Randomly generated string
    """
    level = verify_user(variable)
    logs = get_logs(level)
    return render_template("logs.html", logs=logs)


@app.route('/admin/logs')
@login_required
def admin_logs():
    return render_template("logs.html", level='debug')


@app.route('/new_school', methods=['GET', 'POST'])
@limiter.limit("5/hour;1/minute")
def code_school():
    form = CodeSchoolForm()
    if form.validate_on_submit():
        return handle_submission(form)
    return render_template("code-school.html", title='Code School Request', form=form)


@app.route('/admin/messages', methods=['GET'])
@login_required
def messages():
    return get_messages()


@app.route('/404')
def HTTP404():
    return render_template('status/HTTP404.html'), 404


@app.route('/403')
def HTTP403():
    return render_template('status/HTTP403.html'), 403


@app.route('/410')
def HTTP410():
    return render_template('status/HTTP410.html'), 410


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('HTTP404'))


@app.errorhandler(403)
def page_forbidden(error):
    return redirect(url_for('HTTP403'))


@app.errorhandler(410)
def page_gone(error):
    return redirect(url_for('HTTP410'))
