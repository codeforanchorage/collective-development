from random import randint
from mongoengine import Q, NotUniqueError

from .models import User


# Email and username must be unique
class UserExistsError(Exception): pass


def create_user(username=None, password=None, email=None, is_admin=False, display_name=None):
	""" Creates a new user """
	if not username or not password or not email:
		return None # @todo: exception handling 
	user = User(username=username, password=password, email=email, is_admin=is_admin, display_name=display_name)
	try:
		user.save()
		return user
	except NotUniqueError, e:
		raise UserExistsError('User with email address (%s) or username (%s) or useralready exists' % (email, username))
		return None


def find_user(name):
	""" Gets a user by one of its 2 unique fields: username or email """
	return User.objects.get(Q(username=name) | Q(email=name))


def random_user():
	""" Gets a random user """
	count = User.objects.count()
	return User.objects.limit(-1).skip(randint(0,count-1)).next()


def delete_all_users():
	""" Deletes all the users. Careful! """
	User.drop_collection()