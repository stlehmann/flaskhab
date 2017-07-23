import logging
from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.mongoengine import ModelView
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine
from flask_socketio import SocketIO
from flask_mqtt import Mqtt
from flask_login import LoginManager
from flaskext.lesscss import lesscss
from config import config
from .admin.modelviews import AuthorizedModelView, ControlModelView, \
    NumericControlModelView, RCSwitchControlModelView, CameraControlModelView, \
    MQTTMessageModelView
from .admin.views import AuthorizedAdminIndexView

logger = logging.getLogger(__name__)
bootstrap = Bootstrap()
db = MongoEngine()
socketio = SocketIO()
mqtt = Mqtt()
admin = Admin(template_mode='bootstrap3', index_view=AuthorizedAdminIndexView())
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name: str):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config.from_pyfile('../credentials.py')

    # init extensions
    bootstrap.init_app(app)
    db.init_app(app)
    socketio.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)
    lesscss(app)

    # mqtt initialisation
    mqtt.init_app(app)
    refresh_subsriptions(app)

    # register blueprints
    from .core import core as core_blueprint
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(core_blueprint)
    app.register_blueprint(main_blueprint)

    # register Admin views
    from .models import Switch, Panel, Numeric, RCSwitch, Camera, MQTTMessage
    admin.add_view(NumericControlModelView(Numeric, category='Controls'))
    admin.add_view(RCSwitchControlModelView(RCSwitch, name='RCSwitch', category='Controls'))
    admin.add_view(CameraControlModelView(Camera, name='Camera', category='Controls'))
    admin.add_view(AuthorizedModelView(Panel, name='Panels'))
    admin.add_view(MQTTMessageModelView(MQTTMessage, name='MQTT Messages'))

    return app


def refresh_subsriptions(app):
    from .models import refresh_subscriptions
    refresh_subscriptions()
