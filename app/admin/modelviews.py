from ..models import VALUE_TYPE_BOOL, VALUE_TYPE_INT, VALUE_TYPE_FLOAT, \
    VALUE_TYPE_STRING
from flask_admin.contrib.sqla import ModelView


class MQTTItemView(ModelView):
    column_exclude_list = ['value_bool', 'value_int', 'value_float',
                           'value_string', 'update_time']
    form_excluded_columns = column_exclude_list[:]

    form_choices = {
        'value_type': [
            (VALUE_TYPE_BOOL, 'Boolean'),
            (VALUE_TYPE_INT, 'Integer'),
            (VALUE_TYPE_FLOAT, 'Float'),
            (VALUE_TYPE_STRING, 'String')
        ]
    }

    form_args = {
        'value_type': {
            'coerce': int
        }
    }

    column_choices = form_choices


class PanelView(ModelView):
    pass
