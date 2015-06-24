import datetime

from mongoengine import CASCADE, NULLIFY
from bson import ObjectId

from tps.database import db
from tps.mod_school import School
from tps.mod_user import User


class DAN(db.Document):
	
	school = db.ReferenceField(School, reverse_delete_rule = CASCADE)
	users = db.ListField(db.ReferenceField(User, reverse_delete_rule = NULLIFY))
	is_current = db.BooleanField(default=False)
	start = db.DateTimeField(default=datetime.datetime.now())
	end = db.DateTimeField()


	def age(self):
		""" Age (in days). """
		if self.end:
			diff = self.end - self.start
			return diff.days
		else:
			diff = datetime.datetime.now() - self.start
			return diff.days


	def clone(self, finalize=True):
		if finalize:
			self.end = datetime.datetime.now()
			self.is_current = False
			self.save()
		if '_id' in self.__dict__:
			del self.__dict__['_id']
		if '_created' in self.__dict__:
			del self.__dict__['_created']
		if '_changed_fields' in self.__dict__:
			del self.__dict__['_changed_fields']
		self.id = ObjectId()
		self.start = datetime.datetime.now()
		self.end = None
		self.is_current = True
