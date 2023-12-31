from flask import url_for

from app.todo.models import Todo



def test_post_todos(client, init_database):
    data = {"task": "New Task", "status": False}
    response = client.post(
        url_for('api.create_todo'),
        json=data,
        content_type='application/json'
    )
    assert response.status_code == 201
    new_todo = response.get_json()
    assert new_todo['task'] == 'New Task'
    assert new_todo['status'] is False



def test_update_todo(client, init_database):
    data = {"task": "Updated Task", "status": True}
    response = client.put(
        url_for('api.update_todo', id=1),
        json=data,
        content_type='application/json'
    )
    assert response.status_code == 204

    # Verify that the todo has been updated
    updated_todo = Todo.query.get(1)
    assert updated_todo.task == "Updated Task"
    assert updated_todo.status is True


def test_delete_todo(client, init_database):
    response = client.delete(url_for('api.delete_todo', id=1))
    assert response.status_code == 200

    # Verify that the todo has been deleted
    deleted_todo = Todo.query.get(1)
    assert deleted_todo is None