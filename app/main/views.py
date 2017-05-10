import json
from flask import render_template
from flask_login import login_required
from . import main
from .. import mqtt, socketio
from ..models import BaseControl, Panel


@main.route('/')
@login_required
def index():
    panels = Panel.objects
    return render_template('index.html', panels=panels)


@mqtt.on_message()
def handle_messages(client, userdata, message):
    controls = BaseControl.objects(topic=message.topic)
    for control in controls:
        control.handle_mqtt_message(client, userdata, message)


@socketio.on('control clicked')
def handle_control_clicked(json_str):
    data = json.loads(json_str)
    control = BaseControl.objects(id=data['control_id']).first()

    if control is not None:
        control.handle_event(data)
