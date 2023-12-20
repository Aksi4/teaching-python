from flask import Blueprint

cookies_bp = Blueprint("cookies_bp", __name__, template_folder="templates")

from . import views