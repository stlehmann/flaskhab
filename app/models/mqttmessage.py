from .. import db
from datetime import datetime


class MQTTMessage(db.Document):

    DIRECTION_IN = 'in'
    DIRECTION_OUT = 'out'

    client_id = db.StringField()
    topic = db.StringField()
    payload = db.StringField()
    qos = db.IntField()
    direction = db.StringField(max_length=3)
    timestamp = db.DateTimeField()

    @classmethod
    def remove_old(cls, buf=1000):
        for o in cls.objects.order_by('-timestamp')[buf:]:
            o.delete()


def create_mqttmessage(client, userdata, message, direction,
                       timestamp=datetime.utcnow):

    msg = MQTTMessage()
    msg.client_id = client._client_id.decode()
    msg.topic = message.topic.decode()
    msg.payload = message.payload.decode()
    msg.qos = message.qos
    msg.direction = direction
    msg.timestamp = timestamp

    return msg
