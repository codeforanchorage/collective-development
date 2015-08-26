from dateutil import parser
from flask import Blueprint, g, current_app, render_template, flash, redirect, request, url_for, jsonify, Markup
#from flask.ext.mongoengine.wtf import model_form
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from app.utils import url_for_school, model_form
from app.mod_school import get_school_context
from .forms import AddEventForm, EventForm
from .models import Event, Place
from .services import can_edit_place, can_edit_event, can_create_event, can_edit, can_create


events = Blueprint('events', __name__, url_prefix='/events') # should this be classes?
places = Blueprint('places', __name__, url_prefix='/places')


@events.route('/', methods=['GET'])
def list():
	""" Show a list of all events """
	if g.is_default_school:
		events = Event.objects.filter().order_by('-start')
	else:
		events = Event.objects.filter(schools=g.school).order_by('-start')
	return render_template('event/list.html',
		title=_('Events'),
		events=events)


# @todo: calendar

@events.route('/create', methods=['GET','POST'])
@login_required
@can_create_event
def create():
	""" Create an event (usually, within the context of a proposal) """
	form = AddEventForm(request.form, exclude=['end'])
	#del form.end
	# submit
	if form.validate_on_submit():
		e = Event(
			schools = [g.school,])
		form.populate_obj(e)
		e.save()
		flash(_('The new event has been created. Please edit it here to provide more information like its location, a title, description, etc.'))
		return redirect(url_for('events.edit', id=e.id))
	return render_template('event/create.html',
		title=_('Add a class event'),
		form=form)


@events.route('/<id>', methods=['GET'])
def detail(id):
	""" Show a detail of an event """
	e = Event.objects.get_or_404(id=id)
	c = get_school_context(e)
	if not g.school==c:
		flash(_("You've been redirected to the school where the class is happening."))
		return redirect(url_for_school('events.detail', school=c, id=e.id), code=301)
	# Passing some permissions related functions on to Jinja
	current_app.jinja_env.globals['can_edit'] = can_edit
	return render_template('event/detail.html',
		title = e.title,
		event = e,
		other_events = []) #other_events(e))


@events.route('/<id>/edit', methods=['GET','POST'])
@can_edit_event
def edit(id):
	""" Edit an event """
	e = Event.objects.get_or_404(id=id)
	form = EventForm(request.form, e)
	# submit
	if form.validate_on_submit():
		form.populate_obj(e)
		e.save()
		return redirect(url_for('events.detail', id=e.id))
	return render_template('event/edit.html',
		title=_('Edit a class event'),
		event = e,
		form=form)


# detail (place)


# add a place
