import json
import base64
from flask import render_template_string, url_for
from .. import db, mqtt, socketio
from ..core.mqtt import join_topic
from .basecontrol import BaseControl


class Camera(BaseControl):

    topic = db.StringField(max_length=120)

    def render_html(self):
        return render_template_string(
            '<div class="row">'
            '  <div class="col-xs-12">'
            '    <div class="{% if not pending %}hidden{% endif %} loader"></div>'
            '    <img id="{{ control.id }}cameraImage" class="img-responsive img-camera{% if pending %} hidden{% endif %}" src="{{ url_for(\'static\', filename=\'image.png\') }}">'
            '  </div>'
            '</div>'
            '<div class="row">'
            '  <div class="col-xs-12">'
            '    <button id="{{ control.id }}" class="btn btn-primary">Take a Picture</button>'
            '  </div>'
            '</div>', control=self)

    def render_js(self):
        return render_template_string('\n'.join((
            '$("#{{ control.id }}").click(function() {',
            '  var data = {',
            '    control_id: $(this).attr("id")',
            '  }',
            '  var msg = JSON.stringify(data);',
            '  socket.emit("control clicked", msg)',
            '});',
            'socket.on("received image", function(data) {',
            '  console.log("received image");',
            '  d = new Date();',
            '  $("#{{ control.id }}cameraImage").attr("src", data.filename + "?q=" + d.getTime());',
            '});',
        )), control=self)

    def handle_event(self, data):
        msg = json.dumps({'take_picture': True})
        mqtt.publish(join_topic(self.topic, 'in/take_picture'), msg)

    def handle_mqtt_message(self, client, userdata, message):
        filename = 'image.png'
        filepath = 'app/static/' + filename
        data = json.loads(message.payload.decode())
        image = data.get('image')

        if image is not None:
            with open(filepath, 'wb') as f:
                f.write(base64.b64decode(image.encode()))

            socketio.emit(
                'received image',
                {'filename': 'static/image.png'}
            )

    def get_subscribed_topics(self):
        topic = join_topic(self.topic, 'out/image')
        return [topic]
