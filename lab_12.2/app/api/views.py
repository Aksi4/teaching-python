from flask import jsonify, request

from app.todo.models import Todo
from app import db

from . import api_bp


@api_bp.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    todos_data = [{'id': todo.id, 'title': todo.title, 'description': todo.description, 'complete': todo.complete} for todo in todos]
    return jsonify({'todos': todos_data})


@api_bp.route('/todos', methods=['POST'])
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
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo_data = {'id': todo.id, 'title': todo.title, 'description': todo.description, 'complete': todo.complete}
    return jsonify({'todo': todo_data})


@api_bp.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.json
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.complete = data.get('complete', todo.complete)

    db.session.commit()

    return jsonify({'message': 'Todo updated successfully', 'todo': {'id': todo.id, 'title': todo.title, 'description': todo.description, 'complete': todo.complete}})



@api_bp.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    title = todo.title

    db.session.delete(todo)
    db.session.commit()

    return jsonify({'message': f'Todo "{title}" deleted successfully'})


