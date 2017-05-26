import os
import json
from flask import render_template_string
from .. import db, mqtt
from .. import socketio
from .basecontrol import BaseControl


def join_topic(part1: str, part2: str):
    p1 = part1.rstrip('/')
    p2 = part2.rstrip('/')
    return p1 + '/' + p2


class RCSwitch(BaseControl):
    """
    Features of the Switch2 control:

    * switch a device on or off
    * get a state from a device
    * save the state

    * set a switch on
    * topic to send: home/livingroom/powerswitch/in/
    * payload: '{"remote_id": 1, "switch": 1, "state": "on"}'
    * return message from home/livingroom/powerswitch/out/
    * payload: '{"remote_id": 1, "switch": 1, "state": "on"}'

    """
    STATE_ON = 'on'
    STATE_OFF = 'off'
    STATE_UNKNOEN = 'unknown'

    topic = db.StringField(max_length=120)
    remote_id = db.IntField(min_value=0)
    switch = db.IntField(min_value=0)
    state = db.StringField(max_length=10, default=STATE_OFF)

    def render_html(self):
        return render_template_string(
            '<div class="form-group">'
            '  <label class="control-label item-label col-xs-6">'
            '    {% if control.icon %}'
            '    <img class="icon" src="{{ control.get_icon_url() }}">'
            '    {% endif %}'
            '   {{control.label}}:'
            '  </label>'
            '  <div class="col-xs-6">'
            '    <button id="{{ control.id }}On" type="button" class="control-{{ control.id }} btn {% if control.state == "on" %}btn-active {% else %}btn-default {% endif %}mqtt-control" data-btn="on" data-id="{{ control.id }}">On</button>'
            '    <button id="{{ control.id }}Off" type="button" class="control-{{ control.id }} btn {% if control.state == "off" %}btn-active  {% else %}btn-default {% endif %}mqtt-control" data-btn="off" data-id="{{ control.id }}">Off</button>'
            '  </div>'
            '</div>', control=self)

    def render_js(self):
        return render_template_string(
            'socket.on("mqtt_message_{{ control.id }}", function(data) {\n'
            '  if (data.remote_id == {{ control.remote_id }} && data.switch == {{ control.switch }}) {\n'
            '    if (data.state == "on") {\n'
            '      $("#{{ control.id }}On").addClass("btn-active");\n'
            '      $("#{{ control.id }}On").removeClass("btn-default");\n'
            '      $("#{{ control.id }}Off").removeClass("btn-active");\n'
            '      $("#{{ control.id }}Off").addClass("btn-default");\n'
            '    }\n'
            '    else {\n'
            '      $("#{{ control.id }}On").removeClass("btn-active");\n'
            '      $("#{{ control.id }}On").addClass("btn-default");\n'
            '      $("#{{ control.id }}Off").addClass("btn-active");\n'
            '      $("#{{ control.id }}Off").removeClass("btn-default");\n'
            '    };\n'
            '  }\n'
            '});\n'
            '$(".control-{{ control.id }}").click(function() {\n'
            '  var msg = \'{"control_id": "\' + $(this).data("id") + \'", "btn": "\' + $(this).data("btn") + \'"}\';\n'
            '  socket.emit("control clicked", msg)\n'
            '});\n', control=self
        )

    def handle_event(self, data):
        topic = join_topic(self.topic, 'in')
        # topic = self.topic
        msg_data = {
            'remote_id': self.remote_id,
            'switch': self.switch,
            'state': data['btn']
        }
        msg = json.dumps(msg_data)
        mqtt.publish(topic, msg)

    def handle_mqtt_message(self, client, userdata, message):
        data = json.loads(message.payload.decode())
        if not (data['remote_id'] == self.remote_id and
                data['switch'] == self.switch):

            return

        self.state = data['state']
        self.save()

        socketio.emit(
            'mqtt_message_{}'.format(self.id),
            {
                'remote_id': self.remote_id,
                'switch': self.switch,
                'state': self.state
            }
        )

    def get_subscribed_topics(self):
        topic = join_topic(self.topic, 'out')
        return [topic]
