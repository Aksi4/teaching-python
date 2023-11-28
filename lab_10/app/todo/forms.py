from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired, Email, ValidationError, Regexp, EqualTo


class TodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    complete = BooleanField('Complete')
    submit = SubmitField('Add Todo')


