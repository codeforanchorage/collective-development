from random import randint
from flask.ext.script import Manager, prompt_bool
from faker import Factory

from tps.mod_school import load_school, random_school
from tps.mod_user import random_user
from tps.mod_proposal import random_proposal
from .services import delete_all_collections
from .models import Collection


manager = Manager(usage="Perform TPS collection operations")


@manager.option('-n', '--num', dest='num', default=4)
def fake_collections(num):
	""" Generates num fake collections """
	faker = Factory.create()
	for x in range(int(num)):
		c = Collection(
			proposer = random_user(),
			title = faker.bs(),
			description = faker.text(),
			schools = [random_school(),],
			created = faker.date_time(),
			events = [],
			proposals = [],
			)
		c.save()
		for x1 in range(randint(0,20)):
			c.add_interested_user(random_user())
		for y in range(0,x):
			c.add_proposal(random_proposal())
		print "Created: ", c.title


@manager.option('-c', '--coll', dest='coll_id', default=None)
def display(coll_id):
	try:
		c = Collection.objects.get(id=coll_id)
		print "Collection: ", c.title
		print "Proposals:"
		for p in c.all_proposals():
			print "%s: %s" % (p.id, p.title)
		print "Events:"
		for e in c.all_events():
			print "%s: %s" % (e.start, e.title)
	except:
		print "No such collection."


@manager.command
def delete_all():
	""" Deletes all collections """
	if prompt_bool(
		"Are you sure you want to delete all collections? This cannot be undone."):
		delete_all_collections()
		print "All collections have been deleted"