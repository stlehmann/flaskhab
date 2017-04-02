from flask import current_app
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
