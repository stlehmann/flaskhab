import datetime
from . import db, mqtt

VALUE_TYPE_BOOL = 0
VALUE_TYPE_INT = 1
VALUE_TYPE_FLOAT = 2
VALUE_TYPE_STRING = 3


cvt_fct = {
    VALUE_TYPE_BOOL: bool,
    VALUE_TYPE_INT: int,
    VALUE_TYPE_FLOAT: float,
    VALUE_TYPE_STRING: str
}


class MQTTItem(db.Document):
    name = db.StringField(max_length=40)
    label = db.StringField(max_length=40)
    topic = db.StringField()
    icon = db.StringField()
    suffix = db.StringField(max_length=8)
    update_time = db.DateTimeField()
    value_type = db.IntField(default=VALUE_TYPE_FLOAT)

    value_bool = db.BooleanField()
    value_int = db.IntField()
    value_float = db.DecimalField()
    value_string = db.StringField()

    # value readonly property
    @property
    def value(self):
        if self.value_type == VALUE_TYPE_BOOL:
            return self.value_bool
        elif self.value_type == VALUE_TYPE_INT:
            return self.value_int
        elif self.value_type == VALUE_TYPE_FLOAT:
            return self.value_float
        elif self.value_type == VALUE_TYPE_STRING:
            return self.value_string

    @value.setter
    def value(self, value):
        if self.value_type == VALUE_TYPE_BOOL:
            self.value_bool = bool(value)
        elif self.value_type == VALUE_TYPE_INT:
            self.value_int = int(value)
        elif self.value_type == VALUE_TYPE_FLOAT:
            self.value_float = float(value)
        elif self.value_type == VALUE_TYPE_STRING:
            self.value_string = str(value)
        else:
            return
        self.update_time = datetime.datetime.now()

    def __repr__(self):
        return self.name


class MQTTControl(db.Document):

    CONTROL_TYPE_BUTTON = 1

    name = db.StringField(max_length=40)
    label = db.StringField(max_length=40)
    control_type = db.IntField(default=CONTROL_TYPE_BUTTON)
    topic = db.StringField()
    message = db.StringField()

    def __repr__(self):
        return self.name


# @event.listens_for(db.session, 'before_flush')
# def handle_after_commit(session, flush_context, instances):
#     mqtt.unsubscribe_all()
#     for item in MQTTItem.query:
#         mqtt.subscribe(item.topic)


class Panel(db.Document):
    title = db.StringField(max_length=128, required=True)
    items = db.ListField(db.ReferenceField('MQTTItem'))
    controls = db.ListField(db.ReferenceField('MQTTControl'))

    def __repr__(self):
        return self.title
