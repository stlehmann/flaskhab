from ..models import MQTTControl
from flask_admin.contrib.mongoengine import ModelView


class MQTTItemView(ModelView):
    column_exclude_list = ['value_bool', 'value_int', 'value_float',
                           'value_string', 'update_time']
    form_excluded_columns = column_exclude_list[:]


class MQTTControlView(ModelView):
    form_choices = {
        'control_type': [
            (MQTTControl.CONTROL_TYPE_BUTTON, 'Button'),
        ]
    }

    column_choices = form_choices


class PanelView(ModelView):
    pass
