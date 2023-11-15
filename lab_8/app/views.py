from flask import Flask, request, render_template, session, redirect, url_for, flash, make_response
from app.data import skills
from app import app, db
from datetime import datetime, timedelta
from flask_login import login_user, current_user, login_required, logout_user


from app.forms import ReviewForm, LoginForm, PasswordForm, TodoForm, RegistrationForm
from app.models import Review, Todo, User

import platform
import json


@app.route("/account")
@login_required
def account():
    return render_template("account.html")

@app.route('/logout')

def logout():
    logout_user()
    flash('You have been logged out.', 'success')

    return redirect(url_for('index'))





@app.route('/users')
def users():
    users_list = User.query.all()
    total_users = User.query.count()

    return render_template('users.html', users_list=users_list, total_users=total_users)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('Passwords do not match.', 'error')
            return render_template('register.html', title='Register', form=form)

        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))

        # виведення всіх помилок
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error in {getattr(form, field).label.text}: {error}', 'error')

    return render_template('register.html', title='Register', form=form)

@app.route('/todo', methods=['GET'])
def todo():
    form = TodoForm()
    todo_list = Todo.query.all()
    return render_template("todo.html", todo_list=todo_list, form=form)

@app.route('/add_todo', methods=['POST'])
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

    return redirect(url_for("todo"))



@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    todo.complete = not todo.complete
    db.session.commit()
    flash('Status changed', 'success')
    return redirect(url_for("todo"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    title = todo.title
    db.session.delete(todo)
    db.session.commit()

    flash(f'Removed Todo "{title}".', 'success')
    return redirect(url_for("todo"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)  # Зберігає ідентифікатор користувача у сесії
            flash('Successful login', 'success')
            return redirect(url_for('info'))
        else:
            flash('Incorrect login credentials', 'error')
            return redirect(url_for('login'))



    return render_template('login.html', form=form)


@app.route('/reviews', methods=["GET", "POST"])
def reviews():
    form = ReviewForm()
    if form.validate_on_submit():
        user_email = form.user_email.data
        message = form.message.data

        review = Review(user_email=user_email, message=message)
        db.session.add(review)
        db.session.commit()

        flash('Review submitted successfully', 'success')
        return redirect(url_for('reviews'))

    reviews = Review.query.all()
    return render_template("reviews.html", form=form, reviews=reviews)

@app.context_processor
def inject_global_data():
    global_data = {
        'u_agent': request.headers.get('User-Agent'),
        'OS': platform.system(),
        'time': datetime.now()
    }
    return global_data
@app.route("/")
def index():
    return render_template("index.html")



@app.route("/main")
def main():
    return render_template("main.html")



@app.route('/skill/')
@app.route('/skill/<int:idx>')
def skill(idx=None):
    if idx is not None:
        skill = skills[idx]
        return render_template("skill.html", skill=skill, skills=skills, idx=idx)
    else:
        return render_template("skills.html", skills=skills)

@app.route('/form', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        gmail = request.form.get("gmail")
        message = request.form.get("message")
    else:
        gmail = request.args.get("gmail")
        message = request.args.get("message")

    return render_template("form.html", gmail=gmail, message=message)

with open('app/users.json') as f:
    users_data = json.load(f)




@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' in session:
        form = PasswordForm()

        if form.validate_on_submit():
            new_password = form.new_password.data
            username = session['username']

            if username in users_data:
                users_data[username] = new_password

                with open('app/users.json', 'w') as f:
                    json.dump(users_data, f)
                flash('Password successfully changed to a new one.', 'success')
                return redirect(url_for('info'))

        return render_template('change_password.html', form=form)
    else:
        return redirect(url_for('login'))



saved_cookies = {}
@app.route('/info', methods=['GET', 'POST'])
def info():
    username = session.get('username')
    cookies_data = []

    if username:
        if request.method == 'POST':
            if 'cookie_key' in request.form and 'cookie_value' in request.form and 'cookie_expiration' in request.form:
                cookie_key = request.form['cookie_key']
                cookie_value = request.form['cookie_value']
                cookie_expiration = int(request.form['cookie_expiration'])
                expiration_time = datetime.now() + timedelta(seconds=cookie_expiration)
                saved_cookies[cookie_key] = {
                    'value': cookie_value,
                    'expiration': expiration_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

            for key in list(saved_cookies.keys()):
                if f'delete_{key}' in request.form:
                    del saved_cookies[key]

        for key, cookie_data in saved_cookies.items():
            cookies_data.append((key, cookie_data))

        form = PasswordForm()

        return render_template('info.html', username=username, cookies_data=cookies_data, form=form)
    else:
        return redirect(url_for('login'))

@app.route('/add_cookie', methods=['POST'])
def add_cookie():

    cookie_key = request.form['cookie_key']
    cookie_value = request.form['cookie_value']
    cookie_expiration = int(request.form['cookie_expiration'])

    expiration_time = datetime.now() + timedelta(seconds=cookie_expiration)
    saved_cookies[cookie_key] = {
        'value': cookie_value,
        'expiration': expiration_time.strftime('%Y-%m-%d %H:%M:%S'),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return redirect(url_for('info'))


@app.route('/delete_cookie/<key>', methods=['POST'])
def delete_cookie(key):
    if key in saved_cookies:
        del saved_cookies[key]
        flash(f'The cookie with the key "{key}" has been successfully deleted.', 'success')
    return redirect(url_for('info'))

@app.route('/delete_all_cookies', methods=['POST'])
def delete_all_cookies():
    saved_cookies.clear()
    flash('All cookies have been successfully deleted.', 'success')
    return redirect(url_for('info'))




