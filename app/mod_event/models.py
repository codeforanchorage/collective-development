import datetime
from mongoengine import CASCADE, NULLIFY

from app.database import db
from app.mod_user import User
from app.mod_school import School


class Place(db.Document):
	""" A place where an event might happen """
	name = db.StringField(max_length=255, required=True)
	address = db.StringField()
	geo = db.PointField()
	information = db.StringField()
	schools = db.ListField(db.ReferenceField(School, reverse_delete_rule = NULLIFY))
	creator = db.ReferenceField(User, reverse_delete_rule = NULLIFY)
	created = db.DateTimeField(default=datetime.datetime.now())


	def __str__(self):
		return self.name


class Event(db.Document):
	""" Every event has a single start and end time.
	This class does not handle repeating - it is very simple.
	Instead, it will provide a clone method and the logic of
	repeating or continuing events will be handled by the application."""
	#Required fields
	start = db.DateTimeField(default=datetime.datetime.now(), required=True)
	end = db.DateTimeField()
	title = db.StringField(max_length=255)
	schools = db.ListField(db.ReferenceField(School, reverse_delete_rule = NULLIFY))
	creator = db.ReferenceField(User, reverse_delete_rule = NULLIFY)
	created = db.DateTimeField(default=datetime.datetime.now())
	updated = db.DateTimeField(default=datetime.datetime.now())
	# Optional fields
	short_description = db.StringField(max_length=255)
	description = db.StringField()
	places = db.ListField(db.ReferenceField(Place))


	def save(self, *args, **kwargs):
		""" Update the updated field before saving """
		self.updated = datetime.datetime.now()
		super(Event, self).save(*args,**kwargs)


"""
class RepeatingEvent(Event):
	"" If automated repetition is required, then perhaps this class
	could store the repetition variables (how much time between events,
	any skipped dates, repeat until, etc.) ""
	pass
"""
