from flask import Blueprint

post_bp = Blueprint("post_bp", __name__, template_folder="templates")

from . import views