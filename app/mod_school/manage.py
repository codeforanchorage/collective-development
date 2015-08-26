from flask import current_app
from flask.ext.script import Manager, prompt_bool
from .services import load_school

manager = Manager(usage="Perform TPS school operations")


@manager.option('-s', '--school', dest='school', default=None)
def create(school):
	""" Creates a school """
	if school is None:
		school = current_app.config['DEFAULT_SCHOOL']
	s = load_school(school)
	print "Created: ",school
	



