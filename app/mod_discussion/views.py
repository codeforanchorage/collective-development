from flask import Blueprint, g, current_app, render_template, flash, redirect, request, url_for, jsonify
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from app.utils import url_for_school
from app.mod_school import get_school_context
from .models import Discussion, Comment
from .services import start_discussion
from .forms import AddDiscussionForm, AddCommentForm

# Blueprint definition
discussions = Blueprint('discussions', __name__, url_prefix='/discussions')


@discussions.route('/', methods=['GET'])
def list():
	""" Show a list of all discussions """
	if g.is_default_school:
		discussions = Discussion.objects.filter(published=True).order_by('-created')
	else:
		discussions = Discussion.objects.filter(schools=g.school, published=True).order_by('-created')
	return render_template('discussion/list.html',
		title=_('Discussions'),
		discussions=discussions)


@discussions.route('/<id>', methods=['GET'])
def detail(id):
	""" Show a single discussion, redirecting to the appropriate school if necessary """
	d = Discussion.objects.get_or_404(id=id)
	context = get_school_context(d)
	if not g.school==context:
		flash(_("You've been redirected to where the discussion was created."))
		return redirect(url_for_school('discussions.detail', school=context, id=d.id), code=301)
	other_schools = [school for school in d.schools if not school==context]
	comments = Comment.objects.filter(discussion=d).order_by('-created')
	# Passing some permissions related functions on to Jinja
	#current_app.jinja_env.globals['can_edit_proposal'] = can_edit_proposal
	return render_template('discussion/detail.html',
		title = d.title,
		discussion = d,
		comments = comments,
		other_schools = other_schools)


@discussions.route('/create', methods=['GET','POST'])
@login_required
def create():
	""" Create a new discussion """
	schools = g.all_schools
	form = AddDiscussionForm()
	if form.validate_on_submit():
		d = start_discussion(request.form.get("text"), form=form)
		return redirect(url_for('discussions.detail', id=d.id))
	return render_template('discussion/create.html',
		title=_('Start a discussion'),
		form=form)


@discussions.route('/<id>/comment', methods=['GET','POST'])
@login_required
def add_comment(id):
	""" Add a comment to a discussion """
	d = Discussion.objects.get_or_404(id=id)
	form = AddCommentForm()
	if form.validate_on_submit():
		c = Comment(
			creator = current_user._get_current_object(),
			discussion = d)
		form.populate_obj(c)
		c.save()
		return redirect(url_for('discussions.detail', id=d.id))
	return render_template('discussion/add_comment.html',
		discussion = d,
		title = d.title,
		form = form)
