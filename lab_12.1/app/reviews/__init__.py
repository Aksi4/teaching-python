from flask import Blueprint

reviews_bp = Blueprint("reviews_bp", __name__, template_folder="templates")

from . import views