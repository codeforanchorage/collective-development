"""
New schools:
1. create subdomain record that simply points to this same app
2. by default, it uses 'www' or 'default' (for global)
3. add/ edit a school
"""

from flask import Flask, g, request, url_for
from flask.ext.babel import Babel

from app.utils import pretty_date, format_datetime
from app.database import db
from app import config

from datetime import timedelta

from app.mod_auth import login_manager, auth
from app.mod_school import load_school, load_all_schools, schools
from app.mod_user import users
from app.mod_event import events, places
from app.mod_discussion import discussions
from app.mod_proposal import proposals
from app.mod_collection import collections
from app.mod_interest import interested

def create_app(config=config.dev_config, school_name=None):
	""" The main entry point where the application is created """
	# Create the application
	app = Flask(__name__)    
    # User only logged in for 10 minutes before getting auto logged out
	app.permanent_session_lifetime = timedelta(seconds=600)
	# Default configurations
	app.config.from_object(config)
	# Configuration overrides
	app.config.from_pyfile('../application.cfg', silent=True)
	# In "multi-school" mode, each school is run as a separate app.
	# And each is run under the root directory (eg. domain.net/school)
	if school_name is not None:
		app.config['SCRIPT_NAME'] = '/'+school_name
	app.config['SCHOOL'] = school_name or app.config['DEFAULT_SCHOOL']

	# Register everything
	register_extensions(app)
	register_views(app)
	register_template_filters(app)
	configure_hooks(app)
	return app


def register_extensions(app):
	""" All extensions used by the application are registered here """
	# Register database
	db.init_app(app)
	# Flask Babel for translations
	babel = Babel(app)
	@babel.localeselector
	def get_locale():
		accept_languages = app.config.get('ACCEPT_LANGUAGES')
		return request.accept_languages.best_match(accept_languages)
	# Flask Login
	login_manager.setup_app(app)


def register_views(app):
	""" All views/ routes are registered here """
	app.register_blueprint(auth)
	app.register_blueprint(schools)
	app.register_blueprint(users)
	app.register_blueprint(interested)
	app.register_blueprint(discussions)
	app.register_blueprint(events)
	app.register_blueprint(places)
	app.register_blueprint(proposals)
	app.register_blueprint(collections)


def register_template_filters(app):
	@app.template_filter('time_ago')
	def pretty_date_filter(value):
		return pretty_date(value)
	@app.template_filter('datetime')
	def datetime_filter(value, format='medium'):
		return format_datetime(value, format)
    # Mostly from http://stackoverflow.com/a/18900930/5573838
	from jinja2 import Markup
	_js_escapes = {
        '\\': '\\u005C',
        '\'': '\\u0027',
        '"': '\\u0022',
        '>': '\\u003E',
        '<': '\\u003C',
        '&': '\\u0026',
        '=': '\\u003D',
        '-': '\\u002D',
        ';': '\\u003B',
        u'\u2028': '\\u2028',
        u'\u2029': '\\u2029'
	}
	# Escape every ASCII character with a value less than 32.
	_js_escapes.update(('%c' % z, '\\u%04X' % z) for z in xrange(32))
	@app.template_filter('escapejs')
	def escapejs(value):
		retval = []
		for letter in value:
			if _js_escapes.has_key(letter):
				retval.append(_js_escapes[letter])
			else:
				retval.append(letter)
		return Markup("".join(retval))
	# Register global template functions here too
	#app.jinja_env.globals.update(url_for_school=url_for_school)


def configure_hooks(app):
	@app.before_request
	def before_request():
		# Set the school as an application-wide variable
		g.school = load_school(app.config['SCHOOL'])
		g.all_schools = load_all_schools()
		g.default_school = load_school(app.config['DEFAULT_SCHOOL'])
		g.is_default_school = app.config['SCHOOL']==app.config['DEFAULT_SCHOOL']