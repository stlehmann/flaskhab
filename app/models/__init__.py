from mongoengine import signals
from .. import mqtt
from .user import User
from .basecontrol import BaseControl
from .numeric import Numeric
from .panel import Panel
from .switch import Switch
from .rcswitch import RCSwitch


topic_control_map = {}


def handle_post_save(sender, document, created):
    refresh_subscriptions()


def refresh_subscriptions():
    mqtt.unsubscribe_all()
    topic_control_map.clear()
    for control in BaseControl.objects:
        try:
            for topic in control.get_subscribed_topics():
                item = topic_control_map.get(topic)
                if item is None:
                    item = [control.id]
                else:
                    item.append(control.id)
                topic_control_map[topic] = item
                mqtt.subscribe(topic)
        except AttributeError:
            pass


signals.post_save.connect(handle_post_save)
