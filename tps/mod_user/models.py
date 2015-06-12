import datetime

from werkzeug import check_password_hash, generate_password_hash
from flask.ext.login import UserMixin
from mongoengine import Q

from tps.database import db
from .constants import ROLE_USER, ROLE_ADMIN


class User(db.Document, UserMixin):
	""" A user object that integrates with Flask-Login (via UserMixin and the authenticate method) """

	email = db.EmailField(unique=True)
	username = db.StringField(unique=True, max_length=64)
	display_name = db.StringField(max_length=64)
	password = db.StringField(max_length=255)
	active = db.BooleanField(default=True)
	role = db.IntField(default=ROLE_USER)
	created = db.DateTimeField(default=datetime.datetime.now())

	# following which schools? (list of schools)
	# committee memberships (list)

	def __init__(self, is_admin=False, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
		password = kwargs.get('password', None)
		if not self.id and password is not None:
			self.set_password(password)
		if not self.id and self.display_name is None:
			self.display_name = self.username
		if not self.id and is_admin:
			self.role = ROLE_ADMIN


	def is_admin(self):
		return self.role==ROLE_ADMIN


	def set_password(self, password):
		self.password = generate_password_hash(password)


	def check_password(self, password):
		if self.password is None:
			return False
		return check_password_hash(self.password, password)


	@classmethod
	def authenticate(self, login, password):
		""" Used by my implementation of Flask-Login """
		try:
			user = self.objects.get(Q(username=login) | Q(email=login))
			if user:
				authenticated = user.check_password(password)
			else:
				authenticated = False
			return user, authenticated
		except:
			print(traceback.format_exc())
			return None, False

	def __str__(self):
		return self.display_name
