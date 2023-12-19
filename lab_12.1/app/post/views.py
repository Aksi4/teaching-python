from flask import Flask, request, render_template, session, redirect, url_for, flash, make_response, Blueprint, g, current_app, abort



from datetime import datetime
from werkzeug.utils import secure_filename
from flask_login import login_user, current_user, login_required, logout_user
import secrets
import os
from PIL import Image
from .forms import PostForm
from .models import Post
from app import db



from . import post_bp




@post_bp.route("/post/<int:id>/update", methods=['GET', 'POST'])
def update_post(id):
    post = Post.query.get(id)

    if post.user_id != current_user.id:
        flash('You do not have permission to edit this post', 'error')
        return redirect(url_for('.list_posts'))

    form = PostForm(obj=post)


    if form.validate_on_submit():
        if 'update' in request.form:

            post.title = form.title.data
            post.text = form.text.data
            post.type = form.type.data
            post.enabled = form.enabled.data

            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                post.image_file = picture_file

            db.session.commit()
            flash('Post updated successfully', 'success')
            return redirect(url_for('.view_post', post_id=post.id))

        elif 'delete' in request.form:

            db.session.delete(post)
            db.session.commit()
            flash('Post deleted successfully', 'success')
            return redirect(url_for('.list_posts'))

    return render_template('update_post.html', post=post, form=form)

@post_bp.route("/view_post/<int:post_id>")
def view_post(post_id):
    post = Post.query.get(post_id)
    if post is None or not post.enabled:
        abort(404)

    return render_template('view_post.html', post=post)


@post_bp.route("/list_posts")
def list_posts():
    category = request.args.get('category')
    if category:
        posts = Post.query.filter_by(type=category).all()
    else:
        posts = Post.query.all()
    return render_template("list_posts.html", posts=posts, category=category)

@post_bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():

        picture = form.picture.data

        picture_filename = save_picture(picture)

        new_post = Post(
            title=form.title.data,
            text=form.text.data,
            image_file=picture_filename,
            type=form.type.data,
            enabled=form.enabled.data,
            user_id=current_user.id
        )

        db.session.add(new_post)
        db.session.commit()

        flash('Post created successfully', 'success')
        return redirect(url_for('.list_posts'))

    return render_template('create_post.html', form=form)


def save_picture(form_picture):

    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = secure_filename(f"{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}{file_extension}")

    picture_path = os.path.join(current_app.root_path, 'static', 'post_pics')

    os.makedirs(picture_path, exist_ok=True)

    picture_path = os.path.join(picture_path, picture_filename)
    form_picture.save(picture_path)

    return picture_filename

