from random import randint
from flask import g, abort
from flask.ext.login import current_user

from app.mod_dan import load_dan, user_is_dan, user_is_a_dan
from .models import Place, Event


def events_for_collection(collection):
	""" returns all events in a collection """
	return Event.objects.filter(collections=collection).order_by('-start')


def create_place(*args, **kwargs):
	if not 'creator' in kwargs:
		kwargs['creator'] = current_user._get_current_object()
	p = Place(*args, **kwargs)
	p.save()
	return p


def create_event(*args, **kwargs):
	e = Event(*args, **kwargs)
	e.save()
	return e


def random_place():
	""" Gets a random place """
	count = Place.objects.count()
	return Place.objects.limit(-1).skip(randint(0,count-1)).next()


def random_event():
	""" Gets a random event """
	count = Event.objects.count()
	return Event.objects.limit(-1).skip(randint(0,count-1)).next()


def delete_all_places():
	""" Deletes all the places. Careful! """
	Place.drop_collection()


def delete_all_events():
	""" Deletes all the events. Careful! """
	Event.drop_collection()


#
# Permissions related services
#

def can_create(user=None):
	""" Can a user organize a proposal (adding events to it)?
	Allow the school committee and admins """
	user = user or current_user._get_current_object()
	dan = load_dan(g.school)
	return user_is_dan(user, dan) or user.is_admin()


def can_edit(obj, user=None):
	""" Can a user organize a proposal (adding events to it)?
	Allow the school committee and admins """
	#user = user or current_user._get_current_object()
	#dans = [load_dan(school) for school in obj.schools]
	#return user_is_a_dan(user, dans) or obj.creator==user or user.is_admin()
	if user is None:
		return obj.creator==user
	else:
		return obj.creator==user or user.is_admin()


#
# Permissions decorators
#
from functools import wraps

def can_create_event(fn):
	@wraps(fn)
	def decorated_view(*args, **kwargs):
		# For authorization error it is better to return status code 403
		# and handle it in errorhandler separately, because the user could
		# be already authenticated, but lack the privileges.
		if not can_create():
			abort(403)
		return fn(*args, **kwargs)
	return decorated_view


def can_edit_event(fn):
	@wraps(fn)
	def decorated_view(*args, **kwargs):
		# For authorization error it is better to return status code 403
		# and handle it in errorhandler separately, because the user could
		# be already authenticated, but lack the privileges.
		event = Event.objects.get_or_404(id=kwargs.get('id',0))
		if not can_edit(event):
			abort(403)
		return fn(*args, **kwargs)
	return decorated_view


def can_edit_place(fn):
	@wraps(fn)
	def decorated_view(*args, **kwargs):
		# For authorization error it is better to return status code 403
		# and handle it in errorhandler separately, because the user could
		# be already authenticated, but lack the privileges.
		place = Place.objects.get_or_404(id=kwargs.get('id',0))
		if not can_edit(place):
			abort(403)
		return fn(*args, **kwargs)
	return decorated_view
