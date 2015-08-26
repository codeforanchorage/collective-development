from flask import Blueprint, g, current_app, render_template, flash, redirect, request, url_for, jsonify
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from tps.utils import url_for_school
from tps.mod_school import get_school_context
from .models import Collection

# Blueprint definition
collections = Blueprint('collections', __name__, url_prefix='/collections')


@collections.route('/', methods=['GET'])
def list():
	""" Show a list of all collections """
	if g.is_default_school:
		collections = Collection.objects.filter(published=True).order_by('-created')
	else:
		collections = Collection.objects.filter(schools=g.school, published=True).order_by('-created')
	return render_template('collection/list.html', 
		title=_('Collections'), 
		collections=collections)


@collections.route('/<id>', methods=['GET'])
def detail(id):
	""" Show a single collection, redirecting to the appropriate school if necessary """
	c = Collection.objects.get_or_404(id=id)
	context = get_school_context(c)
	if not g.school==context:
		flash(_("You've been redirected to where the proposal was made."))
		return redirect(url_for_school('collections.detail', school=context, id=c.id), code=301)
	other_schools = [school for school in c.schools if not school==context]
	# Passing some permissions related functions on to Jinja
	#current_app.jinja_env.globals['can_edit_proposal'] = can_edit_proposal
	#current_app.jinja_env.globals['can_organize_proposal'] = can_organize_proposal
	return render_template('collection/detail.html', 
		title = c.title, 
		collection = c,
		proposals = c.all_proposals(),
		events = c.all_events(),
		other_schools = other_schools)


@collections.route('/create', methods=['GET','POST'])
@login_required
def create():
	""" Create a new collection """
	schools = g.all_schools
	form = AddDiscussionForm()
	if form.validate_on_submit():
		d = start_discussion(request.form.get("text"), form=form)
		return redirect(url_for('discussions.detail', id=d.id))
	return render_template('discussion/create.html', 
		title=_('Start a discussion'), 
		form=form)
	