from random import randint
from flask.ext.script import Manager, prompt_bool
from faker import Factory

from app.mod_school import load_school, random_school
from app.mod_user import random_user
from .services import add_comment, delete_all_discussions
from .models import Discussion, Comment


manager = Manager(usage="Perform Collective Development discussion operations")


@manager.option('-n', '--num', dest='num', default=4)
def fake_discussions(num):
	""" Generates num fake discussions """
	from app.mod_proposal import random_proposal
	faker = Factory.create()
	for x in range(int(num)):
		d = Discussion(
			title = faker.bs(),
			schools = [random_school(),],
			creator = random_user(),
			created = faker.date_time(),
			)
		d.save()
		for y in range(randint(0,25)):
			add_comment(faker.text(), random_user(), d, time=faker.date_time())
		p = random_proposal()
		p.add_discussion(d)
		print "Created discussion with ", y ," comments: ", d.title


@manager.command
def delete_all():
	""" Deletes all discussions """
	if prompt_bool(
		"Are you sure you want to delete all discussions? This cannot be undone."):
		delete_all_discussions()
		print "All discussions have been deleted"
