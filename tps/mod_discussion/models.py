import datetime

from bson import ObjectId
from mongoengine import CASCADE, NULLIFY

from tps.utils import pretty_date
from tps.database import db
from tps.mod_user import User
from tps.mod_school import School


class Comment(db.Document):
	"""
	Each individual comment
	"""
	creator = db.ReferenceField(User, reverse_delete_rule = NULLIFY)
	created = db.DateTimeField(default=datetime.datetime.now())
	updated = db.DateTimeField(default=datetime.datetime.now())
	published = db.BooleanField(default=True)
	discussion = db.GenericReferenceField()
	# The actual content of the comment
	text = db.StringField()


class Discussion(db.Document):
	"""
	Thread of comments.
	"""
	title = db.StringField(max_length=255, required=True)
	# The comments and pointers to certain important comments
	#comments = db.SortedListField(db.ReferenceField(Comment), ordering="created", reverse=True)
	num_comments = db.IntField(default=0)
	first_comment = db.ReferenceField(Comment)
	last_comment = db.ReferenceField(Comment)
	last_comment_time = db.DateTimeField(default=datetime.datetime.now())
	# Setting priority might allow for control over the ordering of discussion threads
	priority = db.IntField(default=0)
	created = db.DateTimeField(default=datetime.datetime.now())
	creator = db.ReferenceField(User, reverse_delete_rule = NULLIFY)
	published = db.BooleanField(default=True)
	schools = db.ListField(db.ReferenceField(School, reverse_delete_rule = NULLIFY))


	def add_comment(self, text, user, time=None):
		""" Creates a new comment and adds it to discussion thread """
		c = Comment(
			creator = user,
			text = text,
			created = time or datetime.datetime.now(),
			discussion = self,
			)
		c.save()
		#self.update(add_to_set__comments=c)
		#self.reload()
		#self.update(set__num_comments=len(self.comments))
		if not self.first_comment:
			self.first_comment = c
		self.last_comment = c
		self.last_comment_time = c.created
		self.save()