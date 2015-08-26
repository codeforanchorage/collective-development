"""
A proposal is the basic element of The Public School.
Rather than distinguish between a proposal (virtual) and a class (actual) as 
two different data types, the class is still a proposal.. only, at different "stage".

Similarly, a Collection could have been considered yet another data type.
But a collection could be 'proposed' and it might have been initially throught of 
as a class idea, but it was recognized to function better as a collection.
So, a collection is also a proposal at a different "stage."
"""
import datetime

from bson import ObjectId
from mongoengine import CASCADE, NULLIFY

from tps.database import db
from tps.mod_user import User


class Interested(db.EmbeddedDocument):
	""" Structure for holding information about someone being interested in a proposal """
	date = db.DateTimeField(default=datetime.datetime.now())
	user = db.ReferenceField(User)
	can_teach = db.BooleanField(default=False)
	can_organize = db.BooleanField(default=False)
	can_host = db.BooleanField(default=False)
	

class InterestedMixin(object):
	""" Mixin to provide fields for interest/ following functionality """

	interested = db.ListField(db.EmbeddedDocumentField(Interested))
	num_interested = db.IntField(default=0)


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
	def interested_users(self):
		return [interested.user for interested in self.interested]
