from flask import current_app, request, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_required, current_user
from flask_security import roles_required
from werkzeug.local import LocalProxy

from pyback.web import bp
from pyback.web.forms import CodeSchoolForm
from pyback.web.handlers import handle_submission

logger = LocalProxy(lambda: current_app.logger)

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)


@limiter.request_filter
def ip_whitelist():
    return request.remote_addr in ["127.0.0.1", "localhost"]


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('admin/index.html', title='Home')


@bp.route('/admin/logs')
@login_required
def admin_logs():
    return render_template("web/logs.html")


@bp.route('/new_school', methods=['GET', 'POST'])
@limiter.limit("5/hour;1/minute")
def code_school():
    form = CodeSchoolForm()
    if form.validate_on_submit():
        return handle_submission(form)
    return render_template("web/code-school.html", title='Code School Request', form=form)


@bp.route('/admin/messages', methods=['GET'])
@roles_required('Admin')
def messages():
    logger.info(f'Rendering bot message table for {current_user.email}')
    return render_template('web/messages.html')
