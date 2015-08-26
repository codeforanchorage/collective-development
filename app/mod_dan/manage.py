from flask import current_app
from flask.ext.script import Manager, prompt_bool
from app.mod_school import load_school
from app.mod_user import find_user
from .services import load_dan, add_user_to_dan, remove_user_from_dan, delete_all_dans

manager = Manager(usage="Perform Collective Development committee operations")


@manager.option('-s', '--school', dest='school', default=None)
def show(school):
	""" Shows details of a school's committee """
	if school is None:
		school = current_app.config['DEFAULT_SCHOOL']
	s = load_school(school)
	dan = load_dan(s)
	print "DAN - committee for %s:" % school
	if dan.users:
		for u in dan.users:
			print " - %s <%s>" % (u.username, u.email)
	else:
		print " - There is nobody on the committee now. Use 'add_user -u <user> -s <school>' to add someone."


@manager.option('-u', '--user', dest='user', default=None)
@manager.option('-s', '--school', dest='school', default=None)
def add_user(user, school):
	""" Adds a user to a school's committee """
	print "Loading DAN - committee for %s:" % school
	if school is None:
		school = current_app.config['DEFAULT_SCHOOL']
	s = load_school(school)
	u = find_user(user)
	if u:
		add_user_to_dan(u, load_dan(s))
		print " - added to committee: %s" % user
	else:
		print " - no user exists with email or username: %s" % user


@manager.option('-u', '--user', dest='user', default=None)
@manager.option('-s', '--school', dest='school', default=None)
def remove_user(user, school):
	""" Removes a user from a school's committee """
	print "Loading DAN - committee for %s:" % school
	if school is None:
		school = current_app.config['DEFAULT_SCHOOL']
	s = load_school(school)
	u = find_user(user)
	if u:
		remove_user_from_dan(u, load_dan(s))
		print " - removed from committee: %s" % user
	else:
		print " - no user exists with email or username: %s" % user


@manager.command
def delete_all():
	""" Deletes all users """
	if prompt_bool(
		"Are you sure you want to delete all committees? This cannot be undone."):
		delete_all_dans()
		print "All committees have been deleted"
