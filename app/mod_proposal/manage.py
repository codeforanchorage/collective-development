from random import randint
from flask.ext.script import Manager, prompt_bool
from faker import Factory

from app.mod_school import load_school, random_school
from app.mod_user import random_user
from app.mod_interest import add_user_interest
from .services import delete_all_proposals
from .models import Proposal


manager = Manager(usage="Perform Collective Development proposal operations")


@manager.command
def fake_proposals(num=10):
	"""
		Generates num fake proposals
	"""
	faker = Factory.create()
	for x in range(int(num)):
		p = Proposal(
				proposer=random_user(),
				title=faker.bs(),
				description=faker.text(),
				tags=faker.words(),
				schools=[random_school(),],
				created=faker.date_time(),
				events=[],
			)
		p.save()
		for x in range(randint(0,20)):
			add_user_interest(random_user(), p, Proposal)
		print("Created: {}".format(p.title))


@manager.command
def delete_all():
	""" Deletes all proposals """
	if prompt_bool(
		"Are you sure you want to delete all proposals? This cannot be undone."):
		delete_all_proposals()
		print "All proposals have been deleted"
