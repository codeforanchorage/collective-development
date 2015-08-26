from random import randint
from flask.ext.script import Manager, prompt_bool
from faker import Factory

from app.mod_school import load_school, random_school
from app.mod_user import random_user
from app.mod_proposal import random_proposal
from .services import create_place, create_event, random_place, random_event, delete_all_places, delete_all_events


manager = Manager(usage="Perform Collective Development event operations")


@manager.command
def fake_places(num=10):
	"""
		Generates num fake places
	"""
	faker = Factory.create()
	for x in range(int(num)):
		p = create_place(
				name=faker.text(),
				information=faker.paragraph(),
				address=faker.address(),
				geo=[float(faker.longitude()), float(faker.latitude())],
				schools=[random_school(),],
				creator=random_user(),
				created=faker.date_time(),
			)
		print("Created: {}".format(p.address))


@manager.command
def fake_events(num=10):
	"""
		Generates num fake events
	"""
	faker = Factory.create()
	for x in range(int(num)):
		e = create_event(
				start=faker.date_time(),
				title=faker.bs(),
				schools=[],
				creator=random_user(),
				created=faker.date_time(),
				description=faker.paragraph(),
				short_description=faker.sentence(),
				places=[random_place(),]
			)
		p = random_proposal()
		e.schools = p.schools
		e.save()
		p.add_event(e)
		print("Created: {}\n    (added to proposal: {})".format(e.title, p.title))


@manager.command
def delete_events():
	""" Deletes all events """
	if prompt_bool(
		"Are you sure you want to delete all events? This cannot be undone."):
		delete_all_events()
		print "All events have been deleted"


@manager.command
def delete_places():
	""" Deletes all places """
	if prompt_bool(
		"Are you sure you want to delete all places? This cannot be undone."):
		delete_all_places()
		print "All places have been deleted"
