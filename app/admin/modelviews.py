import os
from config import basedir
from ..models import VALUE_TYPE_BOOL, VALUE_TYPE_INT, VALUE_TYPE_FLOAT, \
    VALUE_TYPE_STRING, MQTTControl
from flask_admin.contrib.mongoengine import ModelView


class MQTTItemView(ModelView):
    column_exclude_list = ['value_bool', 'value_int', 'value_float',
                           'value_string', 'update_time']
    form_excluded_columns = column_exclude_list[:]

    icon_dir = os.path.join(basedir, 'app/static/icons')
    icons = [(x, os.path.splitext(x)[0]) for x in os.listdir(icon_dir) if x[-3:].lower() == 'png']

    form_choices = {
        'value_type': [
            (VALUE_TYPE_BOOL, 'Boolean'),
            (VALUE_TYPE_INT, 'Integer'),
            (VALUE_TYPE_FLOAT, 'Float'),
            (VALUE_TYPE_STRING, 'String'),
        ],
        'icon': icons
    }

    form_args = {
        'value_type': {
            'coerce': int,
        }
    }

    column_choices = form_choices


class MQTTControlView(ModelView):
    form_choices = {
        'control_type': [
            (MQTTControl.CONTROL_TYPE_BUTTON, 'Button'),
        ]
    }

    form_args = {
        'control_type': {
            'coerce': int,
        }
    }
    column_choices = form_choices


class PanelView(ModelView):
    pass
