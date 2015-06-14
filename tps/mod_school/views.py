from flask import Blueprint, g, render_template, flash, redirect, request, url_for
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.babel import gettext as _


school = Blueprint('school', __name__)


@school.route('/', methods=['GET'])
def home():
	return render_template('school/home.html', title='Home', school=g.school)