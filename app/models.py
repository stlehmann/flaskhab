import datetime
from . import db, mqtt
from sqlalchemy import event


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


class MQTTItem(db.Model):
    __tablename__ = 'mqtt_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    label = db.Column(db.String)
    topic = db.Column(db.String)
    icon = db.Column(db.String)
    suffix = db.Column(db.String(8))
    update_time = db.Column(db.DateTime)
    value_type = db.Column(db.Integer, default=VALUE_TYPE_FLOAT)

    value_bool = db.Column(db.Boolean)
    value_int = db.Column(db.Integer)
    value_float = db.Column(db.Float)
    value_string = db.Column(db.String)

    panel_id = db.Column(db.Integer, db.ForeignKey('panels.id'))
    panel = db.relationship('Panel', backref='items')

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


class MQTTControl(db.Model):

    CONTROL_TYPE_BUTTON = 1

    __tablename__ = 'mqtt_controls'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    label = db.Column(db.String)
    control_type = db.Column(db.Integer, default=CONTROL_TYPE_BUTTON)
    topic = db.Column(db.String)
    message = db.Column(db.String)
    panel_id = db.Column(db.Integer, db.ForeignKey('panels.id'))
    panel = db.relationship('Panel', backref='controls')

    def __repr__(self):
        return self.name


@event.listens_for(db.session, 'before_flush')
def handle_after_commit(session, flush_context, instances):
    mqtt.unsubscribe_all()
    for item in MQTTItem.query:
        mqtt.subscribe(item.topic)


class Panel(db.Model):
    __tablename__ = 'panels'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return self.title
