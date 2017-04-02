from flask import render_template
from . import main
from .. import mqtt, socketio
from ..models import MQTTItem, Panel


@main.route('/')
def index():
    panels = Panel.query.all()
    return render_template('index.html', panels=panels)


@mqtt.on_message()
def handle_messages(client, userdata, message):
    with mqtt.app.app_context():
        item = MQTTItem.query.filter_by(topic=message.topic).first()
        if item is not None:
            item.value = message.payload
            socketio.emit(
                'mqtt_message',
                dict(id=item.id, value=item.value,
                     update_time=item.update_time.strftime(
                        'last updated: %d.%m.%Y %H:%M:%S'
                     ))
            )
