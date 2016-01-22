from flask import Blueprint, g, current_app, render_template, flash, redirect, request, url_for, jsonify, abort, Request, Markup
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

#from app.utils import url_for_school
#from app.mod_school import get_school_context
from .models import Discussion, Comment
from .services import start_discussion, can_edit_comment
from .forms import AddDiscussionForm, AddCommentForm, EditCommentForm

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


@discussions.route('/<discussion_id>/proposals/<proposal_id>', methods=['GET'])
def detail(discussion_id, proposal_id):
	""" Show a single discussion, redirecting to the appropriate school if necessary """
	d = Discussion.objects.get_or_404(id=discussion_id)
	#context = get_school_context(d)
	#if not g.school==context:
	#	flash(_("You've been redirected to where the discussion was created."))
	#	return redirect(url_for_school('discussions.detail', school=context, id=d.id), code=301)
	#other_schools = [school for school in d.schools if not school==context]
	comments = Comment.objects.filter(discussion=d).order_by('created')
	# Passing some permissions related functions on to Jinja
	current_app.jinja_env.globals['can_edit_comment'] = can_edit_comment
	return render_template('discussion/detail.html',
		title = d.title,
		discussion = d,
		comments = comments, proposal_id=proposal_id, current_user=current_user)
		#other_schools = other_schools)


#@discussions.route('/create/proposals/<proposal_id>', methods=['GET','POST'])
#def create(proposal_id):
#	if current_user.is_anonymous():
#		flash(Markup("<span class=\"glyphicon glyphicon-info-sign\"></span> You have to login before creating a discussion."), "info")
#		return redirect('/login?next=' + str(request.path))

#	""" Create a new discussion """
#	schools = g.all_schools
#	form = AddDiscussionForm()	
#	if form.validate_on_submit():
#		d = start_discussion(request.form.get("text"), form=form)
#		return redirect(url_for('proposal.detail', discussion_id=d.id, proposal_id=proposal_id))
#	return render_template('discussion/create.html',
#		title=_('Start a discussion'),
#		form=form)


@discussions.route('/<discussion_id>/comment/proposals/<proposal_id>', methods=['GET','POST'])
def add_comment(discussion_id, proposal_id):
	if current_user.is_anonymous():
		flash(Markup("<span class=\"glyphicon glyphicon-info-sign\"></span> You have to login before adding a comment."), "info")
		return redirect('/login?next=' + str(request.path))

	""" Add a comment to a discussion """
	d = Discussion.objects.get_or_404(id=discussion_id)
	form = AddCommentForm()
	if form.validate_on_submit():
		c = Comment(
			creator = current_user._get_current_object(),
			discussion = d)
		import datetime
		c.created = datetime.datetime.now()
		d.last_comment_time = c.created
		form.populate_obj(c)
		c.save()
		d.save()
		return redirect(url_for('discussions.detail', discussion_id=d.id, proposal_id=proposal_id))
	return render_template('discussion/add_comment.html',
		discussion = d,
        proposal_id = proposal_id,
		title = d.title,
		form = form)

@discussions.route('/<discussion_id>/comments/<comment_id>/edit/proposals/<proposal_id>', methods=['GET','POST'])
def edit_comment(discussion_id, comment_id, proposal_id):
	if current_user.is_anonymous():
		flash(Markup("<span class=\"glyphicon glyphicon-info-sign\"></span> You have to login before editing a comment."), "info")
		return redirect('/login?next=' + str(request.path))

	""" Edit a comment of a discussion """
	d = Discussion.objects.get_or_404(id=discussion_id)
	c = Comment.objects.get_or_404(id=comment_id)
	form = EditCommentForm()

	# If the user is not the owner of the comment and not an admin, throw a 403
	if current_user._get_current_object() != c.creator:
		if not current_user.is_admin():
			abort(403)

	if form.validate_on_submit():
		c.edit_comment(newText=form.text.data)
		return redirect(url_for('discussions.detail', discussion_id=d.id, proposal_id=proposal_id))

	return render_template('discussion/edit_comment.html',
		discussion = d,
        proposal_id = proposal_id,
		title = d.title,
		comment = c,
        text = c.text,
        form = form)

@discussions.route('/<discussion_id>/comments/<comment_id>/delete/proposals/<proposal_id>', methods=['GET', 'POST'])
def delete_comment(discussion_id, comment_id, proposal_id):
	if current_user.is_anonymous():
		flash(Markup("<span class=\"glyphicon glyphicon-info-sign\"></span> You have to login before deleting a comment."), "info")
		return redirect('/login?next=' + str(request.path))

	""" Delete a comment of a discussion """
	d = Discussion.objects.get_or_404(id=discussion_id)
	c = Comment.objects.get_or_404(id=comment_id)

	# If the user is not the owner of the comment and not an admin, throw a 403
	if current_user._get_current_object() != c.creator:
		if not current_user.is_admin():
			abort(403)

    # Comment is not actually deleted. We mark that the comment is deleted with a variable to mainintain the text of the comment.
	c.is_deleted = True
	c.save()
	flash(Markup("<span class=\"glyphicon glyphicon-ok\"></span> Comment was successfully deleted."), "success")
	return redirect(url_for('discussions.detail', discussion_id=d.id, proposal_id=proposal_id))
