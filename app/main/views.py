import json
from flask import render_template
from . import main
from .. import mqtt, socketio
from ..models import MQTTItem, MQTTControl, Panel


@main.route('/')
def index():
    panels = Panel.objects
    return render_template('index.html', panels=panels)


@mqtt.on_message()
def handle_messages(client, userdata, message):
    with mqtt.app.app_context():
        item = MQTTItem.objects(topic=message.topic).first()
        if item is not None:
            item.value = message.payload
            item.save()
            socketio.emit(
                'mqtt_message',
                dict(
                    id=str(item.id), value=item.value,
                    update_time=item.update_time.strftime(
                        'last updated: %d.%m.%Y %H:%M:%S')
                )
            )


@socketio.on('control clicked')
def handle_control_clicked(json_str):
    data = json.loads(json_str)
    control = MQTTControl.query.filter_by(name=data['control_id']).first()
    if control is None:
        return

    mqtt.publish(control.topic, control.message)
    print(data)
