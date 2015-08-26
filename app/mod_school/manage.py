from flask import current_app
from flask.ext.script import Manager, prompt_bool
from .services import load_school

manager = Manager(usage="Perform Collective Development school operations")


@manager.command
def create(school=None):
	"""
		Creates a school
	"""
	if school is None:
		school = current_app.config['DEFAULT_SCHOOL']
	_ = load_school(school)
	print("Created: {}".format(school))
