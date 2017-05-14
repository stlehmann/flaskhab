from flask import Blueprint, url_for
core = Blueprint('core', __name__)
from . import filters
