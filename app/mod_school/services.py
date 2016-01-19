from random import randint
from flask import g
from flask.ext.login import current_user

from .models import School


#def get_school_context(obj):
#	""" What is the school that an event or place should appear in? """
#	if not obj.schools:
#		#return None
#		return g.default_school # better to default to default context than None
#	elif len(obj.schools)==1:
#		return obj.schools[0]
#	else:
#		return g.default_school


def load_school(name):
	obj, created = School.objects.get_or_create(name=name)
	return obj


def load_schools(names):
	""" Loads a number of schools by name """
	return School.objects.filter(name__in=names).order_by('name')


def user_schools(user=None):
	""" Usually, you will want to use user.schools, but forms may want a QueryList instead. Use this then """
	user = user or current_user._get_current_object()
	return School.objects(name__in=[school.name for school in user.schools])


def all_schools():
	""" Simply returns all schools in the database """
	return School.objects


def load_all_schools():
	""" All schools, ordered by name (perhaps should be merged into the above?) """
	return School.objects.order_by('name')


def random_school():
	""" Gets a random school """
	count = School.objects.count()
	return School.objects.limit(-1).skip(randint(0,count-1)).next()