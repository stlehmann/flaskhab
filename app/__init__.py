import logging
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
from flaskext.lesscss import lesscss
from config import config


logger = logging.getLogger(__name__)
bootstrap = Bootstrap()
db = MongoEngine()
socketio = SocketIO()
mqtt = Mqtt()
admin = Admin(template_mode='bootstrap3')


def create_app(config_name: str):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('../credentials.py')

    # init extensions
    bootstrap.init_app(app)
    db.init_app(app)
    socketio.init_app(app)
    admin.init_app(app)
    lesscss(app)

    # mqtt initialisation
    mqtt.init_app(app)

    refresh_subsriptions(app)

    # register blueprints
    from .core import core as core_blueprint
    from .main import main as main_blueprint
    app.register_blueprint(core_blueprint)
    app.register_blueprint(main_blueprint)

    # register Admin views
    from .models import Switch, Panel, DecimalValue
    admin.add_view(ModelView(DecimalValue, category='Controls'))
    admin.add_view(ModelView(Switch, name='Switch', category="Controls"))
    admin.add_view(ModelView(Panel, name='Panels'))

    return app


def refresh_subsriptions(app):
    from .models import refresh_subscriptions
    refresh_subscriptions()
