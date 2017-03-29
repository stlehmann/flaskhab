from . import db, socketio


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
    topic = db.Column(db.String)
    suffix = db.Column(db.String(8))
    value_type = db.Column(db.Integer, default=VALUE_TYPE_FLOAT)

    panel_id = db.Column(db.Integer, db.ForeignKey('panels.id'))
    panel = db.relationship('Panel', backref='items')

    _payload = None
    _value = None

    # payload property
    @property
    def payload(self):
        return self._payload

    @payload.setter
    def payload(self, value):
        self._payload = value
        self._value = cvt_fct[self.value_type](value)

    # value readonly property
    @property
    def value(self):
        return self._value

    def __repr__(self):
        return self.name


class Panel(db.Model):
    __tablename__ = 'panels'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
