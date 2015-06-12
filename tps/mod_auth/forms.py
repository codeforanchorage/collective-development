from flask.ext.wtf import Form  
from wtforms import TextField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import Required


class LoginForm(Form):  
	""" Login form """
	next = HiddenField()
	username = TextField('Username', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Sign in')