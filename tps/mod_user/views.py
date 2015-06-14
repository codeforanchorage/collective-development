from flask import Blueprint, g, current_app, render_template, flash, redirect, request, url_for, jsonify
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from tps.utils import url_for_school
from tps.mod_school import get_school_context
from .forms import UserSettingsForm, PasswordForm
from .models import User
from .services import can_edit, can_edit_user


# Blueprint definition
users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/<id>', methods=['GET'])
def detail(id):
	""" Show a single userproposal, redirecting to the appropriate school if necessary """
	u = User.objects.get_or_404(id=id)
	c = get_school_context(u)
	if not g.school==c:
		flash(_("You've been redirected to the school the user is following."))
		return redirect(url_for_school('users.detail', school=c, id=u.id), code=301)
	return render_template('user/detail.html', 
		title = u.display_name, 
		user = u)



@users.route('/edit/<id>', methods=['GET', 'POST'])
@users.route('/edit', methods=['GET', 'POST'])
@can_edit
@login_required
def edit(id=None):
	""" Edit a user """
	if id:
		u = User.objects.get_or_404(id=id)
	else:
		u = current_user._get_current_object()
	form = UserSettingsForm(request.form, u)
	print form.schools
	# submit
	if form.validate_on_submit():
		form.populate_obj(u)
		u.save()
		flash(_("The settings have been saved"), 'success')
	return render_template('user/settings.html', 
		title=_('Edit settings'), 
		user = u,
		form=form)


@users.route('/password', methods=['GET', 'POST'])
@login_required
def password():
	user = current_user._get_current_object()
	form = PasswordForm(next=request.args.get('next'))
	if form.validate_on_submit():
		user.set_password(form.new_password.data)
		user.save()
		flash(_('Password updated.'), 'success')
		return redirect(url_for('users.edit'))
	return render_template('user/password.html', 
		user=user,
		form=form)