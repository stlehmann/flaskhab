from mongoengine import signals
from .. import mqtt
from .user import User
from .basecontrol import BaseControl
from .numeric import Numeric
from .panel import Panel
from .switch import Switch


def handle_post_save(sender, document, created):
    refresh_subscriptions()


def refresh_subscriptions():
    mqtt.unsubscribe_all()
    for control in BaseControl.objects:
        try:
            mqtt.subscribe(control.topic)
        except AttributeError:
            pass


signals.post_save.connect(handle_post_save)