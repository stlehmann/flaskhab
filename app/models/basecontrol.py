from .. import db


class BaseControl(db.Document):

    meta = {'allow_inheritance': True}
    name = db.StringField(max_length=40)
    label = db.StringField(max_length=40)

    def __str__(self):
        return self.name

    def get_subscribed_topics(self):
        return []

    def render_js(self):
        return ''

    def render_html(self):
        return ''