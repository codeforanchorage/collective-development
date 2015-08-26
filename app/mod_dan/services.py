from flask.ext.login import current_user

from app.mod_school import load_schools
from .models import DAN
from .constants import MIN_LIFESPAN


def load_dan(school):
	""" Loads the current committee for a school (creating it if necessary) """
	obj, created = DAN.objects.get_or_create(school=school, is_current=True)
	return obj


def clone_dan(dan, obey_lifespan=True):
	"""  Makes a copy of a committee, closing the current one, if the committee is old enough. """
	if not obey_lifespan or dan.age()>MIN_LIFESPAN:
		return dan.clone()
	else:
		return dan


def user_is_dan(user, dan):
	""" Is the user on the committee? """
	for u in dan.users:
		if u==user:
			return True
	return False


def user_is_a_dan(user, dans):
	""" Is the user on one of the given committees? """
	for dan in dans:
		if user_is_dan(user, dan):
			return True
	return False


def user_dans(user=None, only_current=True):
	""" What committees is the user on? only_current can be False to give historical information """
	user = user or current_user._get_current_object()
	if only_current:
		# Generally we want a queryset here so we do an extra query to be able to returns schools that way
		return load_schools([dan.school.name for dan in DAN.objects.filter(users=user, is_current=True)])
	else:
		return DAN.objects.filter(users=user)


def add_user_to_dan(user, dan):
	""" Adds a user to a committee """
	dan = clone_dan(dan)
	dan.update(add_to_set__users=user)


def add_users_to_dan(users, dan):
	""" Adds a list of users to a committee """
	for user in users:
		add_user_to_dan(user, dan)


def remove_user_from_dan(user, dan):
	""" Removing a user from a committee """
	dan = clone_dan(dan)
	dan.update(pull__users=user)


def remove_users_from_dan(users, dan):
	""" Removes a list of users to a committee """
	dan = clone_dan(dan)
	for user in users:
		remove_user_from_dan(user, dan)


def set_dan(users, dan):
	""" Sets users of a committee (replacing all previous ones) """
	dan = clone_dan(dan)
	dan.users = users
	dan.save()


def delete_all_dans():
	""" Deletes all the committees. Careful! """
	DAN.drop_collection()
