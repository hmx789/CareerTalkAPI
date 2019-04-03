from flask import Blueprint
bp = Blueprint('main', __name__)
from careertalk.main import routes
