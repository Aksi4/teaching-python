from app.auth.models import User
from app.post.models import Post
from app.todo.models import Todo
from app import db


def test_user_model():
    """
    GIVEN a user model
    WHEN a new user is created
    THEN check the email and password fields are defined correctly
    """

    user = User(username="user", email="user@example.com", password="password")
    assert user.username == 'user'
    assert user.email == 'user@example.com'
    assert user.password != 'password'


def test_todo_model():
    """
    GIVEN a todo model
    WHEN a new todo is created
    THEN check the title and description fields are defined correctly
    """
    todo = Todo(title="todo py", description="Some description")
    assert todo.task == "todo py"


def test_post_model():
    """
    GIVEN a Post model
    WHEN a new Post is created
    THEN check the ...... are defined correctly
    """

    post = Post(title='Lorem ipnsun post', text='tihs is my post zxc qwerty')
    assert post.title == 'Lorem ipnsun post'
    assert post.text == 'tihs is my post zxc qwerty'