from flask import render_template, current_app
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
            old_val = item.value
            item.value = message.payload
            new_val = item.value
            if old_val != new_val:
                socketio.emit(
                    'mqtt_message', dict(id=item.id, value=item.value)
                )
