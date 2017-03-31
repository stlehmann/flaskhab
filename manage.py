import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import create_app, db


app = create_app(os.environ.get('FLASK_CONFIG', 'default'))
manager = Manager(app)
migrate = Migrate(app, db)

from app.models import MQTTItem

def make_shell_context():
    return dict(app=app, db=db, MQTTItem=MQTTItem)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def run(host='0.0.0.0', port=5000, use_reloader=False):
    port = int(port)
    from app import socketio
    socketio.run(app, host=host, port=port, use_reloader=use_reloader)

if __name__ == '__main__':
    manager.run()