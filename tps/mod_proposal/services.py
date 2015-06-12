from random import randint

from flask import g, abort
from flask.ext.login import current_user
from tps.mod_dan import load_dan, user_is_a_dan
from .models import Proposal, Interested


def add_user_interest(user, proposal, extra=None):
	""" Modifying user interested 
	'extra' can be None or 'can_teach', 'can_organize', 'can_host' """
	if not proposal.user_is_interested(user):
		proposal.add_interested_user(user)
	elif extra in ['can_teach', 'can_organize', 'can_host']:
		kw = {'set__interested__S__'+extra: True}
		Proposal.objects(id=proposal.id, interested__user=user).modify(**kw)


def remove_user_interest(user, proposal, only=None):
	""" Remove user from being interested in this proposal
	If 'only' is set to a fieldname, then only that fieldname is set to False """
	if only is None:
		proposal.remove_interested_user(user)
	elif only in ['can_teach', 'can_organize', 'can_host']:
		kw = {'set__interested__S__'+only: False}
		Proposal.objects(id=proposal.id, interested__user=user).modify(**kw)


def random_proposal():
	""" Gets a random proposal """
	count = Proposal.objects.count()
	return Proposal.objects.limit(-1).skip(randint(0,count-1)).next()


def delete_all_proposals():
	""" Deletes all the proposals. Careful! """
	Proposal.drop_collection()


#
# Permissions related services
#

def can_edit_proposal(proposal, user=None):
	""" Can a user edit a particular proposal? 
	Allow the proposal author, the school committee members, and admins """
	user = user or current_user._get_current_object()
	dans = [load_dan(school) for school in proposal.schools]
	return user_is_a_dan(user, dans) or proposal.proposer==user or user.is_admin()


def can_organize_proposal(proposal, user=None):
	""" Can a user organize a proposal (adding events to it)?
	Allow the school committee and admins """
	user = user or current_user._get_current_object()
	dans = [load_dan(school) for school in proposal.schools]
	return user_is_a_dan(user, dans) or user.is_admin()


# 
# Permissions decorators
#
from functools import wraps

def can_edit(fn):
	@wraps(fn)
	def decorated_view(*args, **kwargs):
		# For authorization error it is better to return status code 403
		# and handle it in errorhandler separately, because the user could
		# be already authenticated, but lack the privileges.
		proposal = Proposal.objects.get_or_404(id=kwargs.get('id',0))
		if not can_edit_proposal(proposal):
			abort(403)
		return fn(*args, **kwargs)
	return decorated_view

def can_organize(fn):
	@wraps(fn)
	def decorated_view(*args, **kwargs):
		# For authorization error it is better to return status code 403
		# and handle it in errorhandler separately, because the user could
		# be already authenticated, but lack the privileges.
		proposal = Proposal.objects.get_or_404(id=kwargs.get('id',0))
		if not can_organize_proposal(proposal):
			abort(403)
		return fn(*args, **kwargs)
	return decorated_view