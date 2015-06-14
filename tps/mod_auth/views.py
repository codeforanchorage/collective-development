from flask import Blueprint, render_template, flash, redirect, request, url_for
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.babel import gettext as _

from tps.mod_auth import authenticate_user
from tps.mod_school import get_school_context
from .forms import LoginForm

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated():
		return redirect(url_for('proposals.make'))
	form = LoginForm(username=request.args.get('username', None), next=request.args.get('next', None))
	if form.validate_on_submit():
		user, authenticated = authenticate_user(form.username.data, form.password.data)
		if user and authenticated:
			remember = request.form.get('remember') == 'y'
			if login_user(user, remember=remember):
				flash(_("Logged in"), 'success')
			return redirect(form.next.data or 'proposals/make')
		else:
			flash(_('Sorry, invalid login'), 'error')			
	return render_template('auth/login.html', title='login', form=form)


@auth.route('/reauth', methods=['GET', 'POST'])
@login_required
def reauth():
	return "reauth"


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash(_('Logged out'), 'success')
	return redirect(url_for('proposals.list'))

