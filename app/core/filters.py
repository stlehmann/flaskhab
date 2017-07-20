import os
from flask import current_app, url_for
from . import core


@core.app_context_processor
def inject_variables():
    return dict(SSL=current_app.config['SSL'])


@core.app_template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    if date is None:
        return '-'
    native = date.replace(tzinfo=None)
    fmt = fmt or '%d.%m.%Y %H:%M:%S'
    return native.strftime(fmt)


@core.app_context_processor
def override_url_for():
    return dict(
        url_for=dated_url_for
    )


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(current_app.root_path,
                                     endpoint, filename)
            if os.path.exists(file_path):
                values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
