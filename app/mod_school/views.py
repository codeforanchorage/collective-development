from flask import Blueprint, g, render_template, flash, redirect, request, url_for, abort
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.babel import gettext as _

from .models import School
from .forms import SchoolForm

schools = Blueprint('schools', __name__)

@schools.route('/', methods=['GET'])
def home():
	return render_template('school/home.html', title='Home', school=g.school)

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