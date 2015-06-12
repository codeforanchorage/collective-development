from flask import g
from random import randint
from .models import School


def get_school_context(obj):
	""" What is the school that an event or place should appear in? """
	if not obj.schools:
		#return None
		return g.default_school # better to default to default context than None
	elif len(obj.schools)==1:
		return obj.schools[0]
	else:
		return g.default_school


def all_schools():
	return School.objects


def load_school(name):
	obj, created = School.objects.get_or_create(name=name)
	return obj


def load_all_schools():
	return School.objects.order_by('name')


def random_school():
	""" Gets a random school """
	count = School.objects.count()
	return School.objects.limit(-1).skip(randint(0,count-1)).next()