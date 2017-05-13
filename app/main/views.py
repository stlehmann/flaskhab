import json
from flask import render_template
from flask_login import login_required
from . import main
from .. import mqtt, socketio
from ..models import BaseControl, Panel, topic_control_map


@main.route('/')
@login_required
def index():
    panels = Panel.objects
    return render_template('index.html', panels=panels)


@mqtt.on_message()
def handle_messages(client, userdata, message):
    control_ids = topic_control_map.get(message.topic)
    if control_ids is None:
        return

    controls = BaseControl.objects(id__in=control_ids)
    for control in controls:
        control.handle_mqtt_message(client, userdata, message)


@socketio.on('control clicked')
def handle_control_clicked(json_str):
    data = json.loads(json_str)
    control = BaseControl.objects(id=data['control_id']).first()

    if control is not None:
        control.handle_event(data)
