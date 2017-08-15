

from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, SubmitField
from wtforms.validators import Required, Length, Email, DataRequired


class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class SignupForm(Form):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField("Log In")

