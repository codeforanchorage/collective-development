from flask import Blueprint, g, current_app, render_template, flash, redirect, request, url_for, jsonify
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from tps.utils import url_for_school
from tps.mod_school import get_school_context
from tps.mod_event import events_for_proposal
from .forms import AddProposalForm, ProposalForm
from .models import Proposal
from .services import can_edit, can_organize, can_edit_proposal, can_organize_proposal, add_user_interest, remove_user_interest

# Blueprint definition
proposals = Blueprint('proposals', __name__, url_prefix='/proposals')


@proposals.route('/', methods=['GET'])
def list():
	""" Show a list of all proposals """
	if g.is_default_school:
		proposals = Proposal.objects.filter(published=True).order_by('-created')
	else:
		proposals = Proposal.objects.filter(schools=g.school, published=True).order_by('-created')
	return render_template('proposal/list.html', 
		title=_('Proposals'), 
		proposals=proposals)


@proposals.route('/<id>', methods=['GET'])
def detail(id):
	""" Show a single proposal, redirecting to the appropriate school if necessary """
	p = Proposal.objects.get_or_404(id=id)
	c = get_school_context(p)
	if not g.school==c:
		flash(_("You've been redirected to where the proposal was made."))
		return redirect(url_for_school('proposals.detail', school=c, id=p.id), code=301)
	other_schools = [school for school in p.schools if not school==c]
	# Passing some permissions related functions on to Jinja
	current_app.jinja_env.globals['can_edit_proposal'] = can_edit_proposal
	current_app.jinja_env.globals['can_organize_proposal'] = can_organize_proposal
	return render_template('proposal/detail.html', 
		title = p.title, 
		proposal = p,
		other_schools = other_schools,
		events = events_for_proposal(p))


@proposals.route('/make', methods=['GET', 'POST'])
@login_required
def make():
	""" Make a proposal route """
	schools = g.all_schools
	if g.is_default_school and len(g.all_schools())>0:
		return render_template('proposal/make_choose_school.html', 
			title=_('Which school?'), 
			schools=[school for school in schools if not school==g.default_school])
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
@login_required
@can_edit
def edit(id):
	""" Edit an event """
	p = Proposal.objects.get_or_404(id=id)
	form = ProposalForm(request.form, p)
	# submit
	if form.validate_on_submit():
		form.populate_obj(p)
		e.save()
		return redirect(url_for('proposals.detail', id=p.id))
	return render_template('proposal/edit.html', 
		title=_('Edit a proposal'), 
		proposal = p,
		form=form)


@proposals.route('/<id>/organize', methods=['GET', 'POST'])
@login_required
@can_organize
def organize(id):
	return "organizing!"


@proposals.route('/<id>/interest', methods=['POST'])
@login_required
def interest(id):
	""" Toggles current user's interest in a proposal """
	p = Proposal.objects.get_or_404(id=id)
	u = current_user._get_current_object()
	remove = request.form.get('action','add')=='remove'
	attribute = request.form.get('attribute', None) or None
	print attribute
	if remove:
		remove_user_interest(u, p, only=attribute)
	else:
		add_user_interest(u, p, extra=attribute)
	return jsonify({
		'num_interested':p.num_interested, 
		'next' : 'remove' if p.user_is_interested(u) else 'add'
		})


	