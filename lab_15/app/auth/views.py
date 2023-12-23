from flask import Flask, request, render_template, session, redirect, url_for, flash, make_response, Blueprint, g





from flask_login import login_user, current_user, login_required, logout_user
import secrets
import os
from PIL import Image
from .forms import PasswordChangeForm, AccountUpdateForm, LoginForm, RegistrationForm
from .models import User
from app import db



from . import auth_bp




@auth_bp.before_request
def before_request():
    g.db = db

@auth_bp.teardown_request
def teardown_request(exception=None):
    db = getattr(g, 'db', None)
    if db is not None:
        db.session.close()

@auth_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():


    password_form = PasswordChangeForm()
    update_account_form = AccountUpdateForm()


    if request.method == 'POST':
        if 'update_account_submit' in request.form:
            return update_account()
        elif 'change_password_submit' in request.form:
            return change_password()

    return render_template("account.html", password_form=password_form, update_account_form=update_account_form)
@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordChangeForm()

    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('auth_bp.account'))
        else:
            flash('Incorrect current password.', 'error')
            return redirect(url_for('auth_bp.account'))


    return render_template('account.html', password_form=form)


@auth_bp.route('/update_account', methods=['GET', 'POST'])
@login_required
def update_account():
    form = AccountUpdateForm()


    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data

        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        session['username'] = current_user.username
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('auth_bp.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me


    # помилки
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{field.capitalize()}: {error}', 'error')
            return redirect(url_for('auth_bp.account'))

    return render_template('account.html', title='Update Account', update_account_form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(auth_bp.root_path, 'static/profile_pics', picture_fn)

    output_size = (1280, 1280)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():


    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            flash('Successful login', 'success')
            session['username'] = username
            return redirect(url_for('cookies_bp.info'))
        else:
            flash('Incorrect login credentials', 'error')
            return redirect(url_for('.login'))

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')

    return redirect(url_for('.login'))

@auth_bp.route('/users_all')
def users_all():
    users_list = User.query.all()
    total_users = User.query.count()

    return render_template('users.html', users_list=users_list, total_users=total_users)

@auth_bp.route("/register", methods=['GET', 'POST'])
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
        return redirect(url_for('auth_bp.login'))

        # помилки
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Error in {getattr(form, field).label.text}: {error}', 'error')

    return render_template('register.html', title='Register', form=form)





