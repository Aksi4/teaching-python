from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, InputRequired, Email, ValidationError, Regexp, EqualTo
from flask_wtf.file import FileField, FileAllowed
from .models import Post
from flask_login import current_user

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    picture = FileField('Picture', validators=[FileAllowed(['jpg', 'png'])])
    type = SelectField('Type', choices=[('news', 'News'), ('publication', 'Publication'), ('other', 'Other')],
                       default='news', validators=[DataRequired()])
    enabled = BooleanField('Enabled', default=True)
    submit = SubmitField('Submit')



