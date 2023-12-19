from flask import render_template, redirect, url_for, flash, g
from app import db

from .forms import TodoForm
from .models import Todo

from . import todo_bp

@todo_bp.before_request
def before_request():
    g.db = db

@todo_bp.teardown_request
def teardown_request(exception=None):
    db = getattr(g, 'db', None)
    if db is not None:
        db.session.close()

@todo_bp.route('/todo', methods=['GET'])
def todo():
    form = TodoForm()
    todo_list = Todo.query.all()
    return render_template("todo.html", todo_list=todo_list, form=form)

@todo_bp.route('/add_todo', methods=['POST'])
def add_todo():
    form = TodoForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        complete = form.complete.data
        new_todo = Todo(title=title, description=description, complete=complete)
        db.session.add(new_todo)
        db.session.commit()
        flash('New todo added successfully', 'success')

    return redirect(url_for(".todo"))



@todo_bp.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    flash('Status changed', 'success')
    return redirect(url_for(".todo"))


@todo_bp.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    title = todo.title
    db.session.delete(todo)
    db.session.commit()

    flash(f'Removed Todo "{title}".', 'success')
    return redirect(url_for(".todo"))








