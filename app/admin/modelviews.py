from flask_admin.contrib.mongoengine import ModelView
from flask_admin.form import rules
from flask_login import current_user
from jinja2 import Markup


class AuthorizedModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated


class ControlModelView(AuthorizedModelView):

    column_exclude_list = ['_cls']

    def _list_icon(view, context, model, name):
        if not model.icon:
            return ''

        return Markup(
            '<img src="{}" style="max-width: 30px; max-height: 30px;">'.format(model.get_icon_url())
        )

    column_formatters = {
        'icon': _list_icon,
    }

    form_rules = [
        'name', 'label', 'icon',
        rules.HTML(
            '<div class="form-group">'
            '<div class="col-md-10 col-md-offset-2">'
            '<img id="iconImg" class="icon" src="#">'
            '</div>'
            '</div>'
        )
    ]

    edit_template = 'admin/edit_control.html'


class NumericControlModelView(ControlModelView):

    form_rules = ControlModelView.form_rules + [
        'topic',
        'precision',
        'suffix'
    ]


class RCSwitchControlModelView(ControlModelView):

    form_rules = ControlModelView.form_rules + [
        'topic',
        'remote_id',
        'switch'
    ]


class CameraControlModelView(ControlModelView):

    form_rules = ControlModelView.form_rules + [
        'topic',
    ]

