from flask import render_template, current_app
from . import main
from .. import mqtt, socketio
from ..models import MQTTItem, Panel


@main.context_processor
def inject_variables():
    return dict(SSL=current_app.config['SSL'])


@main.app_template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    native = date.replace(tzinfo=None)
    fmt = fmt or '%d.%m.%Y %H:%M:%S'
    return native.strftime(fmt)


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
