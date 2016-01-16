from flask import Blueprint, g, render_template, flash, redirect, request, url_for, abort
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.babel import gettext as _

from .models import School
from .forms import SchoolForm

schools = Blueprint('schools', __name__)

@schools.route('/', methods=['GET'])
def home():
    from app.mod_event import Event
    from app.mod_proposal import Proposal

    if g.is_default_school:
        events = Event.objects.filter().order_by('-start')
    else:
        events = Event.objects.filter(schools=g.school).order_by('-start')

    if g.is_default_school:
        proposals = Proposal.objects.filter(published=True).order_by('-created')
    else:
        proposals = Proposal.objects.filter(schools=g.school, published=True).order_by('-created')

    return render_template('school/home.html', school=g.school, events=events, proposals=proposals)

@schools.route('/schools/add', methods=['GET', 'POST'])
def add_school():
    if not current_user.is_admin():
        abort(403)
    
    form = SchoolForm()
    if form.validate_on_submit():		
        s = School()
        form.populate_obj(s)
        s.save()
        return redirect(url_for('schools.add_school'))
    return render_template('school/add_school.html', form=form)