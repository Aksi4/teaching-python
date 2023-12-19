from flask import url_for
from flask_login import login_user
from .base_test import BaseTest
from app import db
from app.todo.models import Todo
from app.auth.models import User

class TodoTest(BaseTest):

    def test_todo_create(self):
        data = {
            'task': 'Write flask tests',
        }


        user = User(username= 'random_user', email='random_user@email.com', password='123456789')
        db.session.add(user)
        db.session.commit()

        with self.client:

            login_user(user)

            response = self.client.post(
                url_for('todo.todo'),
                data=data,
                follow_redirects=True
            )

            todo = Todo.query.filter_by(task='Write flask tests').first()

            if todo is not None:
                print(f"Todo ID: {todo.id}, Todo Task: {todo.task}")
            else:
                print("Todo object is None")

            print(f"Response Status Code: {response.status_code}")
            print(f"Response Data: {response.data.decode('utf-8')}")

            assert response.status_code == 200
            assert todo is not None
            assert todo.task == data['task']

    def test_update_todo_complete(self):
        todo_1 = Todo(task="todo1", status=False)
        db.session.add(todo_1)
        db.session.commit()

        with self.client:
            response = self.client.get(
                url_for('todo.update_todo', id=todo_1.id),
                follow_redirects=True
            )

            todo = db.session.query(Todo).get(todo_1.id)

            print(f"Before Update - Todo Status: {todo.status}")

            todo.status = True
            db.session.commit()

            todo = db.session.query(Todo).get(todo_1.id)

            print(f"After Update - Todo Status: {todo.status}")

            assert response.status_code == 200
            assert todo is not None
            assert todo.status == True


    def test_delete_todo(self):
        data = {
            'task': 'Write flask tests',
        }

        with self.client:
            self.client.post(
                url_for('todo.todo'),
                data=data,
                follow_redirects=True
            )

            response = self.client.get(
                url_for('todo.delete_todo', id=1),
                follow_redirects=True
            )

            todo = Todo.query.filter_by(id=1).first()

            print(f"Deleted Todo: {todo}")

            assert response.status_code == 200
            assert todo is None