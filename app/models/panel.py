from .. import db


class Panel(db.Document):
    title = db.StringField(max_length=128, required=True)
    controls = db.ListField(db.ReferenceField('BaseControl'))

    def __str__(self):
        return self.title
