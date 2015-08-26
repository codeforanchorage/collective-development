import datetime
from flask import g, url_for
from flask.ext.login import current_user
import flask.ext.babel as babel

from .form import model_form, BaseForm
from tps.mod_school import get_school_context


def url_for_school(endpoint, school=None, user_school=False, **values):
	""" Similar to typical url for, except this will rewrite the base to the specified school """
	url = url_for(endpoint, **values)
	csn = g.school.name # current school name
	fsn = school.name if hasattr(school,'name') else school # future school name
	if fsn is None and user_school:
		u = current_user._get_current_object()
		c = get_school_context(u)
		if c:
			fsn = c.name
	# The name of the default school never appears in the path: it is always the base url
	if school == g.default_school:
		fsn = None
	# Requesting the default/ global school
	if fsn is None: 
		if g.is_default_school:
			return url
		else:
			return url.replace('/'+csn, '', 1)
	# Requesting a particular school 
	else:
		if csn==fsn:
			return url
		elif g.is_default_school:
			return url.replace('/', '/'+fsn+'/', 1)
		else:
			return url.replace('/'+csn, '/'+fsn, 1)


def pretty_date(dt, default=None):
	"""
	Returns string representing "time since" e.g.
	3 days ago, 5 hours ago etc.
	Ref: https://bitbucket.org/danjac/newsmeme/src/a281babb9ca3/newsmeme/
	"""

	if default is None:
		default = 'just now'

	now = datetime.datetime.now()
	diff = now - dt

	periods = (
		(diff.days / 365, 'year', 'years'),
		(diff.days / 30, 'month', 'months'),
		(diff.days / 7, 'week', 'weeks'),
		(diff.days, 'day', 'days'),
		(diff.seconds / 3600, 'hour', 'hours'),
		(diff.seconds / 60, 'minute', 'minutes'),
		(diff.seconds, 'second', 'seconds'),
	)

	for period, singular, plural in periods:

		if not period:
			continue

		if period == 1:
			return u'%d %s ago' % (period, singular)
		else:
			return u'%d %s ago' % (period, plural)

	return default


def format_datetime(value, format='medium'):
	""" Provide jinja templates with a way of formatting dates """
	if format == 'custom1':
		format="EEEE, d. MMMM y 'at' HH:mm"
	elif format == 'custom2':
		format="EE dd.MM.y HH:mm"
	return babel.dates.format_datetime(value, format)