"""
Model representing a school
"""

from tps.database import db

class School(db.Document):
	name = db.StringField(max_length=64, required=True)
	title = db.StringField(max_length=255)
	about = db.StringField()
	styles = db.StringField()

	def __str__(self):
		return self.name