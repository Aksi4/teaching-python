from flask import render_template, redirect, url_for, flash
from app import db

from .forms import ReviewForm
from .models import Review

from . import reviews_bp

@reviews_bp.route('/reviews', methods=["GET", "POST"])
def reviews():
    form = ReviewForm()
    if form.validate_on_submit():
        user_email = form.user_email.data
        message = form.message.data

        review = Review(user_email=user_email, message=message)
        db.session.add(review)
        db.session.commit()

        flash('Review submitted successfully', 'success')
        return redirect(url_for('.reviews'))

    reviews = Review.query.all()
    return render_template("reviews.html", form=form, reviews=reviews)



