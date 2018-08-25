from flask import url_for, request, abort
from flask_admin.contrib import sqla
from flask_login import current_user
from werkzeug.utils import redirect

from pyback import admin, db
from pyback.database.models import User, Role, Channel


class MyModelView(sqla.ModelView):
    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('Admin'):
            return True

        return False

    def _handle_view(self, name, **kwargs):
        """
        Override builtin _handle_view in order to redirect users when a view is not accessible.
        """
        if not self.is_accessible():
            if current_user.is_authenticated:
                # permission denied
                abort(403)
            else:
                # login
                return redirect(url_for('security.login', next=request.url))


admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(Channel, db.session))
