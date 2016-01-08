"""
Model representing a school
"""

from app.database import db

class School(db.Document):
	name = db.StringField(max_length=64, required=True)

	def __str__(self):
		return self.name
