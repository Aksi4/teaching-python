from flask import jsonify, request
from flask_httpauth import HTTPBasicAuth
from app.todo.models import Todo
from app import db
from flask_jwt_extended import create_access_token, jwt_required
from app.auth.views import User

from . import api_bp


auth = HTTPBasicAuth()


@auth.verify_password
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return username


@api_bp.route('/login_api', methods=['POST'])
@auth.login_required
def auth_login():
    access_token = create_access_token(identity=auth.current_user())
    return jsonify(access_token=access_token)

@auth.error_handler
def auth_error(status):
    return jsonify(message="Authorization error"), status

@api_bp.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    todos = Todo.query.all()
    todos_data = [{'id': todo.id, 'title': todo.title, 'description': todo.description, 'complete': todo.complete} for todo in todos]
    return jsonify({'todos': todos_data})


@api_bp.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    complete = data.get('complete', False)

    new_todo = Todo(title=title, description=description, complete=complete)
    db.session.add(new_todo)
    db.session.commit()

    return jsonify({'message': 'Todo created successfully', 'todo': {'id': new_todo.id, 'title': new_todo.title, 'description': new_todo.description, 'complete': new_todo.complete}})


@api_bp.route('/todos/<int:todo_id>', methods=['GET'])
@jwt_required()
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo_data = {'id': todo.id, 'title': todo.title, 'description': todo.description, 'complete': todo.complete}
    return jsonify({'todo': todo_data})


@api_bp.route('/todos/<int:todo_id>', methods=['PUT'])
@jwt_required()
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.json
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.complete = data.get('complete', todo.complete)

    db.session.commit()

    return jsonify({'message': 'Todo updated successfully', 'todo': {'id': todo.id, 'title': todo.title, 'description': todo.description, 'complete': todo.complete}})



@api_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    title = todo.title

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': f'Todo "{title}" deleted successfully'})


