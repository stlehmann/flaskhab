from flask import render_template_string
from .. import db, mqtt
from .basecontrol import BaseControl


class Switch(BaseControl):

    btn1_label = db.StringField(max_length=40)
    btn1_topic = db.StringField(max_length=120)
    btn1_message = db.StringField(max_length=120)
    btn2_label = db.StringField(max_length=40)
    btn2_topic = db.StringField(max_length=120)
    btn2_message = db.StringField(max_length=120)

    def render(self):
        return render_template_string(
            '<div class="form-group">'
            '  <label class="control-label item-label col-xs-6">'
            '   {{control.label}}:'
            '  </label>'
            '  <div class="col-xs-6">'
            '    <button id="{{ control.id }}" type="button" class="btn btn-default mqtt-control" data - btn=1 > {{control.btn1_label}} </button>'
            '    <button id="{{ control.id }}" type="button" class="btn btn-default mqtt-control" data - btn=2 > {{control.btn2_label}} </button>'
            '  </div>'
            '</div>', control=self)

    def handle_event(self, data):
        if data['btn'] == 1:
            mqtt.publish(self.btn1_topic, self.btn1_message)
        elif data['btn'] == 2:
            mqtt.publish(self.btn2_topic, self.btn2_message)