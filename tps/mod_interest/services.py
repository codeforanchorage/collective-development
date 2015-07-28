from flask import g, abort
from flask.ext.login import current_user


def add_user_interest(user, obj, cls, extra=None):
	""" Modifying user interested 
	'extra' can be None or 'can_teach', 'can_organize', 'can_host' """
	if not obj.user_is_interested(user):
		obj.add_interested_user(user)
	elif extra in ['can_teach', 'can_organize', 'can_host']:
		kw = {'set__interested__S__'+extra: True}
		cls.objects(id=obj.id, interested__user=user).modify(**kw)


def remove_user_interest(user, obj, cls, only=None):
	""" Remove user from being interested in this proposal
	If 'only' is set to a fieldname, then only that fieldname is set to False """
	if only is None:
		obj.remove_interested_user(user)
	elif only in ['can_teach', 'can_organize', 'can_host']:
		kw = {'set__interested__S__'+only: False}
		cls.objects(id=obj.id, interested__user=user).modify(**kw)