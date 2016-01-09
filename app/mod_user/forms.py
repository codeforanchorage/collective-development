from flask import session
from flask.ext.login import current_user
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import Required, Length, EqualTo, ValidationError
#from flask.ext.mongoengine.wtf import model_form

from app.utils.form import model_form, BaseForm
from .models import User
from .constants import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX
from .services import find_user


def validate_password(form, field):
	""" Checks if the existing password is correct """
	user = current_user._get_current_object()
	if not user.check_password(field.data):
		raise ValidationError("Password is wrong.")


def validate_username(form, field):
	""" Checks if the username is already in use """
	user = current_user._get_current_object()
	current = user.username if hasattr(user,'username') else None
	if not current==field.data and find_user(field.data):
		raise ValidationError("That username is already in use.")


def validate_email(form, field):
	""" Checks if the email is already in use """
	user = current_user._get_current_object()
	current = user.email if hasattr(user,'email') else None
	if not current==field.data and find_user(field.data):
		raise ValidationError("That email address is already in use.")


def validate_gotcha(form, field):
	""" Checks if the gotcha field matches what is set in the session (the view sets the challenge) """
	if not field.data.lower()==session['gotcha'].lower():
		raise ValidationError("Sorry, that's not correct.")


class PasswordForm(BaseForm):
	""" Replace password form """
	password = PasswordField('Current password', [Required(), validate_password])
	new_password = PasswordField('New password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
	password_again = PasswordField('Password again', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX), EqualTo('new_password')])
	submit = SubmitField(u'Update password')


class BaseAddUserForm(BaseForm):
	""" Base add user form """
	field_order = ('username', 'email', '*', 'captcha', 'gotcha', 'submit')
	new_password = PasswordField('New password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
	password_again = PasswordField('Password again', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX), EqualTo('new_password')])
	gotcha = TextField('Gotcha', [validate_gotcha])


UserSettingsForm = model_form( User,
	base_class=Form,
	exclude=(
		'username',
		'password',
		'role',
		'created',
		'active'),
	field_args = {
		'email': { 'validators': [validate_email]} ,
		'schools': { 'label': 'Schools you are following'}
		})
submit_add = SubmitField('Save')
UserSettingsForm.submit = submit_add


UserAddForm = model_form( User,
	base_class=BaseAddUserForm,
	exclude=(
		'password',
		'role',
		'created',
		'active'),
	field_args = {
		'username': { 'validators': [Required(), validate_username]} ,
		'email': { 'validators': [Required(), validate_email]} ,
		'schools': { 'label': 'Schools you are interested in'}
		})
submit_add = SubmitField('Sign up')
UserAddForm.submit = submit_add
