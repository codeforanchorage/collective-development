"""
A proposal is the basic element of The Public School.
Rather than distinguish between a proposal (virtual) and a class (actual) as
two different data types, the class is still a proposal.. only, at different "stage".
"""
import datetime

from bson import ObjectId
from mongoengine import CASCADE, NULLIFY

from app.utils import pretty_date
from app.database import db
from app.mod_user import User
from app.mod_school import School
from app.mod_event import Event
from app.mod_discussion import Discussion
from app.mod_interest import InterestedMixin, Interested

from .constants import LIFE_ORIGIN, LIFE_PLANNING, LIFE_CLASS, LIFE_FINISHED, SOURCE_UNKNOWN, SOURCE_WEBSITE, SOURCE_API, SOURCE_OFFLINE


class Stage(db.EmbeddedDocument):
	""" Structure for holding the stage of a proposal """
	date = db.DateTimeField(default=datetime.datetime.now())
	value = db.IntField(default=LIFE_ORIGIN)
	creator = db.ReferenceField(User)

	@property
	def pretty_date(self):
		return pretty_date(self.date)


class BaseProposal(db.Document, InterestedMixin):
	meta = {
		'allow_inheritance': True,
		'abstract': True,
	}

	title = db.StringField(max_length=255)
	# A copy of the original description is kept
	description = db.StringField()
	edited_description = db.StringField()
	# School the proposal was made to
	schools = db.ListField(db.ReferenceField(School, reverse_delete_rule = NULLIFY))
	# Person who made the proposal
	proposer = db.ReferenceField(User, reverse_delete_rule = NULLIFY)
	created = db.DateTimeField(default=datetime.datetime.now())
	updated = db.DateTimeField(default=datetime.datetime.now())
	published = db.BooleanField(default=True)
	# The proposal that this proposal "copies"
	copy_of = db.ReferenceField("self", reverse_delete_rule = NULLIFY)
	# Events
	events = db.ListField(db.ReferenceField(Event, reverse_delete_rule = NULLIFY))
	# Discussions
	discussions = db.ListField(db.ReferenceField(Discussion, reverse_delete_rule = NULLIFY))


	def add_event(self, event):
		self.update(add_to_set__events=event)
		self.reload()

	def remove_event(self, event):
		self.update(pull__events=event)
		self.reload()

	def add_discussion(self, discussion):
		self.update(add_to_set__discussions=discussion)
		self.reload()

	def remove_discussion(self, discussion):
		self.update(pull__discussions=discussion)
		self.reload()

	def __str__(self):
		return self.title



class Proposal(BaseProposal):
	""" A proposal object """
	meta = {'collection': 'proposal'}
	# Tags
	tags = db.ListField(db.StringField(max_length=30))
	# School the proposal was made to
	schools = db.ListField(db.ReferenceField(School, reverse_delete_rule = NULLIFY))
	# Context in which the proposal was made
	source = db.IntField(default=SOURCE_WEBSITE)
	# Which stage in the organizing process
	stage = db.ListField(db.EmbeddedDocumentField(Stage))


	def __init__(self, *args, **kwargs):
		super(Proposal, self).__init__(*args, **kwargs)
		if not self.id:
			self.interested.append(Interested(user=self.proposer))
			self.num_interested = 1
			self.stage.append(Stage(creator=self.proposer, date=self.created))


	@property
	def current_stage(self):
		current_stage = None
		for s in self.stage:
			if current_stage is None or s.date>current_stage.date:
				current_stage = s
		return current_stage
