import os
from flask import url_for
from config import basedir
from .. import db


class BaseControl(db.Document):

    icon_dir = os.path.join(basedir, 'app/static/icons')
    icons = [(x, os.path.splitext(x)[0])
             for x in os.listdir(icon_dir) if x[-3:].lower() == 'png']

    meta = {'allow_inheritance': True}
    name = db.StringField(max_length=40)
    label = db.StringField(max_length=40)
    icon = db.StringField(choices=icons)

    def __str__(self):
        return self.name

    def get_subscribed_topics(self):
        return []

    def get_icon_url(self):
        if self.icon is None:
            return
        return url_for("static", filename="icons/" + self.icon)

    def render_js(self):
        return ''

    def render_html(self):
        return ''
