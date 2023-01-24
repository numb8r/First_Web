from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class LoginFrom(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password1 = PasswordField('Repaat password', validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField('Remember Me!')
    submit = SubmitField('Sing in')


class PhoneFrom(FlaskForm):
    phone = StringField('Phone', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Sing in')
