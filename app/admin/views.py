from flask import redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_login import current_user


class AuthorizedAdminIndexView(AdminIndexView):

    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return super().index()
