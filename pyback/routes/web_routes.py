import os

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_required
from werkzeug.utils import secure_filename

from pyback import app

from flask import render_template, redirect, url_for, request, jsonify

from pyback.handlers.handle_code_school import handle_recaptcha_and_errors, handle_code_school
from pyback.handlers.slash_command_handlers import render_logs
from pyback.utils.forms import CodeSchoolForm

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


@app.route('/school', methods=['GET', 'POST'])
@limiter.limit("5/hour;1/minute")
def school():
    form = CodeSchoolForm()
    if form.validate_on_submit():
        f = form.logo.data
        filename = secure_filename(f.filename)
        filepath = os.path.join(app.static_folder, 'logos', filename)
        f.save(filepath)
        return jsonify(
            {"redirect": 'https://github.com/AllenAnthes/Database-Project-Front-end/issues', 'code': 302})

    return render_template("school.html", title='Code School Request', form=form)


@app.route('/404')
def HTTP404():
    return render_template('status/HTTP404.html'), 404


@app.route('/403')
def HTTP403():
    return render_template('status/HTTP403.html'), 403


@app.route('/410')
def HTTP410():
    return render_template('status/HTTP410.html'), 410


@app.route('/admin/logs')
@login_required
def admin_logs():
    return render_logs('debug')


@app.errorhandler(404)
def page_not_found(error):
    return redirect(url_for('HTTP404'))


@app.errorhandler(403)
def page_forbidden(error):
    return redirect(url_for('HTTP403'))


@app.errorhandler(410)
def page_gone(error):
    return redirect(url_for('HTTP410'))
