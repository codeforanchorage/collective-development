from faker import Factory
from flask.ext.script import Manager, prompt_bool
from .services import create_user, delete_all_users, UserExistsError

manager = Manager(usage="Perform Collective Development user operations")


@manager.option('-n', '--name', dest='name', default='collectivedevelopment')
@manager.option('-p', '--password', dest='password', default='collectivedevelopment')
@manager.option('-e', '--email', dest='email', default='collectivedevelopment@mailinator.com')
def create_admin(name, password, email):
	""" Creates an administrative user """
	try:
		u = create_user(username=name, password=password, email=email, is_admin=True)
		print "Admin created! username: %s, password: %s, email: %s" % (name, password, email)
	except UserExistsError, e:
		print "A user already exists with that username or email address"


@manager.option('-n', '--name', dest='name', default='collectivedevelopment')
@manager.option('-p', '--password', dest='password', default='collectivedevelopment')
@manager.option('-e', '--email', dest='email', default='collectivedevelopment@mailinator.com')
def create(name, password, email):
	""" Creates a regular user """
	try:
		u = create_user(username=name, password=password, email=email, is_admin=False)
		print "User created! username: %s, password: %s, email: %s" % (name, password, email)
	except UserExistsError, e:
		print "A user already exists with that username or email address"


@manager.option('-n', '--num', dest='num', default=10)
def fake_users(num):
	""" Generates num fake users """
	faker = Factory.create()
	for x in range(int(num)):
		try:
			u = create_user(username=faker.user_name(), password="collectivedevelopment", email=faker.email(), is_admin=False, display_name=faker.name())
			print "User created! name: %s, username: %s, email: %s" % (u.display_name, u.username, u.email)
		except UserExistsError, e:
			pass # ohwell


@manager.command
def delete_all():
	""" Deletes all users """
	if prompt_bool(
		"Are you sure you want to delete all users? This cannot be undone."):
		delete_all_users()
		print "All users have been deleted. You should run 'dan delete_all' now"
