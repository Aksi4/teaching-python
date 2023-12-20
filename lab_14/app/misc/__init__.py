from flask import Blueprint

misc_bp = Blueprint("misc_bp", __name__, template_folder="templates")

from . import views