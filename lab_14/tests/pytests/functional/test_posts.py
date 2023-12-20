from flask import url_for
from flask_login import current_user
from app.auth.models import User
from app.post.models import Post
from app import db



def test_get_all_posts(log_in_default_user, init_database):
    number_of_todos = Post.query.count()
    assert number_of_todos == 2

