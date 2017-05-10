import os
import sys
from flask_script import Manager, Shell
from app import create_app, db


if 'run' in sys.argv:
    import eventlet
    eventlet.monkey_patch()


app = create_app(os.environ.get('FLASK_CONFIG', 'default'))
manager = Manager(app)


import app.models as models


def make_shell_context():
    return dict(app=app, db=db, models=models)


manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def run(host='0.0.0.0', port=5000, use_reloader=True):
    port = int(port)
    from app import socketio
    socketio.run(app, host=host, port=port, use_reloader=use_reloader)


@manager.command
def test():
    os.system('python -m unittest discover -s tests')


if __name__ == '__main__':
    manager.run()
