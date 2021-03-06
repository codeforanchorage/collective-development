from mongoengine import Q
from flask import Blueprint, g, current_app, render_template, flash, redirect, request, url_for, jsonify, Response, Markup, abort
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

#from app.utils import url_for_school
#from app.mod_school import get_school_context
from app.mod_event import AddEventForm, Event
from app.mod_discussion import Discussion, Comment, AddDiscussionForm, start_discussion
from .forms import AddProposalForm, ProposalForm, OrganizeProposalForm
from .models import Proposal
from .services import can_edit, can_organize, can_edit_proposal, can_organize_proposal


# Blueprint definition
proposals = Blueprint('proposals', __name__, url_prefix='/proposals')


@proposals.route('/', methods=['GET'])
def list():
	""" Show a list of all proposals """
	if g.is_default_school:
		proposals = Proposal.objects.filter(published=True).order_by('-created')
	else:
		proposals = Proposal.objects.filter(schools=g.school, published=True).order_by('-created')

	resp = Response(render_template('proposal/list.html',
		title=_('Proposals'),
		proposals=proposals, current_user=current_user))

    # Disable cache on this page (checkmarks need to update properly)
	#resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	#resp.headers['Pragma'] = 'no-cache'

	return resp;


@proposals.route('/search')
def search():
	query = request.args.get('query', "")
	if g.is_default_school:
		proposals = Proposal.objects.filter(Q(published=True)&(Q(title__icontains=query)|Q(description__icontains=query))).order_by('-created')
	else:
		proposals = Proposal.objects.filter(Q(schools=g.school)&Q(published=True)&(Q(title__icontains=query)|Q(description__icontains=query))).order_by('-created')
	return render_template('proposal/list.html',
		title=_('Search results'),
		proposals=proposals, query=query)


@proposals.route('/<id>', methods=['GET'])
def detail(id):
	""" Show a single proposal, redirecting to the appropriate school if necessary """
	p = Proposal.objects.get_or_404(id=id)
	#c = get_school_context(p)
	#if not g.school==c:
	#	flash(_("You've been redirected to where the proposal was made."))
	#	return redirect(url_for_school('proposals.detail', school=c, id=p.id), code=301)
	#other_schools = [school for school in p.schools if not school==c]
	# Passing some permissions related functions on to Jinja
	current_app.jinja_env.globals['can_edit_proposal'] = can_edit_proposal
	current_app.jinja_env.globals['can_organize_proposal'] = can_organize_proposal
	resp = Response(render_template('proposal/detail.html',
		title = p.title,
		proposal = p,
		#other_schools = other_schools,
		events = p.events,
		discussions = p.discussions,
		current_user = current_user, current_url=request.path))
    # Disable cache on this page (toggle button needs to update properly)
	#resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
	#resp.headers['Pragma'] = 'no-cache'

	return resp


@proposals.route('/make', methods=['GET', 'POST'])
def make():
	if current_user.is_anonymous():
		flash(Markup("<span class=\"glyphicon glyphicon-info-sign\"></span> You have to login before creating a proposal."), "info")
		return redirect('/login?next=' + str(request.path))
	
	""" Make a proposal """
	form = AddProposalForm()
	if form.validate_on_submit():
		p = Proposal(schools=[g.school,], proposer=current_user._get_current_object())
		form.populate_obj(p)
		p.save()
		return redirect(url_for('proposals.detail', id=p.id))
	return render_template('proposal/make.html',
		title=_('Make a proposal'),
		form=form)


@proposals.route('/<id>/edit', methods=['GET', 'POST'])
def edit(id):
	if current_user.is_anonymous():
		flash(Markup("<span class=\"glyphicon glyphicon-info-sign\"></span> You have to login before editing a proposal."), "info")
		return redirect('/login?next=' + str(request.path))

	""" Edit an proposal """
	p = Proposal.objects.get_or_404(id=id)
	form = ProposalForm(request.form, p)

	if not current_user.is_admin() and current_user.id == p.proposer.id:        
		interested_list = p.interested[:] # Deep copy to manipulate
		for interested in interested_list:
			if interested.user.id == current_user.id:
				interested_list.remove(interested)
		if len(interested_list) > 0:
			flash(Markup("<span class=\"glyphicon glyphicon-info-sign\"></span> You cannot edit a proposal that has interested users."), "info")
			return redirect(url_for('proposals.detail', id=p.id))

	# submit
	if form.validate_on_submit():
		form.populate_obj(p)
		import datetime
		p.updated = datetime.datetime.now()
		p.save()
		return redirect(url_for('proposals.detail', id=p.id))
	return render_template('proposal/edit.html',
		title=_('Edit a proposal'),
		proposal = p,
		form=form)


@proposals.route('/<id>/organize', methods=['GET', 'POST'])
@can_organize
def organize(id):
	if current_user.is_anonymous():
		flash(Markup("<span class=\"glyphicon glyphicon-info-sign\"></span> You have to login before organizing a proposal."), "info")
		return redirect('/login?next=' + str(request.path))

	p = Proposal.objects.get_or_404(id=id)

	# Throw 403 if user isn't an admin
	if not current_user.is_admin():
		abort(403)

    # You can only organize proposals with interested users
	if p.num_interested == 0:
		flash(Markup("<span class=\"glyphicon glyphicon-exclamation-sign\"></span> You cannot " 
        + "organize a proposal that has no interested users."), "danger")
		return redirect(url_for('proposals.detail', id=p.id))

	form = OrganizeProposalForm()
	if form.validate_on_submit():
		e = Event()
		e.creator = current_user._get_current_object()
		form.populate_obj(e)
		e.save()	
		#p.delete()
		return redirect(url_for('events.detail', id=e.id))

	return render_template("proposal/organize.html", form=form, proposal_title=p.title, proposal_description=p.description)

@proposals.route('/<id>/delete', methods=['DELETE'])
@can_organize
def delete(id):
	if current_user.is_anonymous():
		flash(Markup("<span class=\"glyphicon glyphicon-info-sign\"></span> You have to login before deleting a proposal."), "info")
		return redirect('/login?next=' + str(request.path))

	import json
	p = Proposal.objects.get_or_404(id=id)

	# Throw 403 if user isn't an admin
	if not current_user.is_admin():
		abort(403)
	
	p.delete()
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@proposals.route('/<id>/create/discussion', methods=['GET','POST'])
def create_discussion(id):
	if current_user.is_anonymous():
		flash(Markup("<span class=\"glyphicon glyphicon-info-sign\"></span> You have to login before creating a discussion."), "info")
		return redirect('/login?next=' + str(request.path))

	""" Create a new discussion within the proposal """
	p = Proposal.objects.get_or_404(id=id)
	form = AddDiscussionForm()
	if form.validate_on_submit():
		d = start_discussion(request.form.get("text"), schools=p.schools, form=form)
		p.add_discussion(d)
		return redirect(url_for('discussions.detail', discussion_id=d.id, proposal_id=p.id))
	return render_template('discussion/create.html',
		title=_('New discussion in @title', title=p.title),
		form=form)

@proposals.route('/<id>/add_anon_email/<email>', methods=['POST'])
def add_anon_email(id, email):
	p = Proposal.objects.get_or_404(id=id)
	p.anon_emails.append(email)
	p.save()
	#flash(Markup("<span class=\"glyphicon glyphicon-ok\"></span> The email \"" + email + "\" will be contacted if enough interest is generated for this proposal."), "success")
	import json
	return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@proposals.route('/<id>/teach_class', methods=['POST'])
def teach_class(id):
	if current_user.is_anonymous():
		flash(Markup("<span class=\"glyphicon glyphicon-info-sign\"></span> You have to login before becoming a teacher."), "info")
		return redirect('/login?next=/proposals/' + id)
	
	p = Proposal.objects.get_or_404(id=id)

	for teacher in p.teachers:
		if teacher.id == current_user.id:
			flash(Markup("<span class=\"glyphicon glyphicon-info-sign\"></span> You have already volunteered to become a teacher for this proposal."), "info")
			return detail(id)
	
	p.teachers.append(current_user.to_dbref())
	p.save()
	flash(Markup("<span class=\"glyphicon glyphicon-ok\"></span> Thank you for volunteering to become a teacher for this proposal. We will contact you if there is enough interest generated for this proposal."), "success")
	return detail(id)

#@proposals.route('/<id>/create/event', methods=['GET','POST'])
#@login_required
#@can_organize
#def create_event(id):
#	""" Create an event (usually, within the context of a proposal) """
#	p = Proposal.objects.get_or_404(id=id)
#	form = AddEventForm(request.form, exclude=['end'])
#	# submit
#	if form.validate_on_submit():
#		e = Event(
#			schools = p.schools)
#		form.populate_obj(e)
#		e.save()
#		p.add_event(e)
#		flash(_('The new event has been created. Please edit it here to provide more information like its location, a title, description, etc.'))
#		flash(Markup(_('Or you can do that later and now just add more events by clicking <a href="%(url)s">here</a>', url=url_for('events.create', proposal_id=p.id))))
#		return redirect(url_for('events.edit', id=e.id))
#	return render_template('event/create.html',
#		title=_('Add a class event'),
#		form=form)
