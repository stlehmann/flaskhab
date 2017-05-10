from flask_admin.contrib.mongoengine import ModelView
from flask_login import current_user


class AuthorizedModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated


class NumericModelView(AuthorizedModelView):

    column_exclude_list = ['_cls']