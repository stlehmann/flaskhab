from .. import db


class BaseControl(db.Document):

    meta = {'allow_inheritance': True}
    name = db.StringField(max_length=40)
    label = db.StringField(max_length=40)

    def __str__(self):
        return self.name
