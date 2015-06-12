import datetime

from bson import ObjectId
from mongoengine import CASCADE, NULLIFY

from tps.utils import pretty_date
from tps.database import db
from tps.mod_user import User
from tps.mod_school import School

from .constants import LIFE_ORIGIN, LIFE_PLANNING, LIFE_CLASS, LIFE_FINISHED, SOURCE_UNKNOWN, SOURCE_WEBSITE, SOURCE_API, SOURCE_OFFLINE


class Stage(db.EmbeddedDocument):
	""" Structure for holding the stage of a proposal """
	date = db.DateTimeField(default=datetime.datetime.now())
	value = db.IntField(default=LIFE_ORIGIN)
	creator = db.ReferenceField(User)

	@property
	def pretty_date(self):
		return pretty_date(self.date)


class Interested(db.EmbeddedDocument):
	""" Structure for holding information about someone being interested in a proposal """
	date = db.DateTimeField(default=datetime.datetime.now())
	user = db.ReferenceField(User)
	can_teach = db.BooleanField(default=False)
	can_organize = db.BooleanField(default=False)
	can_host = db.BooleanField(default=False)
	

class Proposal(db.Document):
	""" A proposal object """
	title = db.StringField(max_length=255)
	# A copy of the original description is kept
	description = db.StringField()
	edited_description = db.StringField()
	# Tags
	tags = db.ListField(db.StringField(max_length=30))
	# School the proposal was made to
	schools = db.ListField(db.ReferenceField(School, reverse_delete_rule = NULLIFY))
	# Person who made the proposal
	proposer = db.ReferenceField(User, reverse_delete_rule = NULLIFY)
	created = db.DateTimeField(default=datetime.datetime.now())
	updated = db.DateTimeField(default=datetime.datetime.now())
	published = db.BooleanField(default=True)
	source = db.IntField(default=SOURCE_WEBSITE)
	stage = db.ListField(db.EmbeddedDocumentField(Stage))
	# Users who are interested
	interested = db.ListField(db.EmbeddedDocumentField(Interested))
	num_interested = db.IntField(default=0)
	# The proposal that this proposal "copies"
	copy_of = db.ReferenceField("self", reverse_delete_rule = NULLIFY)


	def __init__(self, *args, **kwargs):
		super(Proposal, self).__init__(*args, **kwargs)
		if not self.id:
			self.interested.append(Interested(user=self.proposer))
			self.num_interested = 1
			self.stage.append(Stage(creator=self.proposer, date=self.created))


	def add_interested_user(self, user):
		self.update(add_to_set__interested=Interested(user=user))
		self.reload()
		self.update(set__num_interested=len(self.interested))
		self.reload()


	def remove_interested_user(self, user):
		self.update(pull__interested__user=user)
		self.reload()
		self.update(set__num_interested=len(self.interested))
		self.reload()


	def user_is_interested(self, user):
		if user is None:
			return False
		for iu in self.interested:
			if iu.user==user:
				return iu
		return False


	@property
	def current_stage(self):
		current_stage = None
		for s in self.stage:
			if current_stage is None or s.date>current_stage.date:
				current_stage = s
		return current_stage


	@property
	def interested_users(self):
		return [interested.user for interested in self.interested]


	def __str__(self):
		return self.title