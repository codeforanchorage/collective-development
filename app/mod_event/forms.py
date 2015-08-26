from flask import g
from flask.ext.mongoengine.wtf.fields import QuerySetSelectMultipleField
from wtforms import TextField, BooleanField, SubmitField, HiddenField
from wtforms.validators import Required
#from flask.ext.mongoengine.wtf import model_form

from tps.utils.form import model_form, BaseForm
from tps.mod_dan import user_dans
from .models import Event, Place
from .services import create_place


class PlacesListField(QuerySetSelectMultipleField):
	""" Allows new places to be created if they don't already exist in the query set """
	def __init__(self, *args, **kwargs):
		super(PlacesListField, self).__init__(*args, **kwargs)
		self.queryset = Place.objects.filter(schools=g.school)
		
	def create_place(self, name):
		return create_place(name=name, schools=[g.school,])

	def process_formdata(self, valuelist):
		if valuelist:
			if valuelist[0] == '__None':
				self.data = None
			else:
				if not self.queryset:
					self.data = None
					return
				self.queryset.rewind()
				self.data = [obj for obj in self.queryset if str(obj.id) in valuelist]
				# figure out any new places
				self.queryset.rewind()
				place_ids = [str(obj.id) for obj in self.queryset]
				self.data.extend([self.create_place(name) for name in valuelist if name not in place_ids])
				print self.data
				if not len(self.data):
					self.data = None



class EventBase(BaseForm):
	""" Full event form """
	submit = SubmitField('Save')
	field_order = ('*', 'places', 'submit')
	places = PlacesListField('Place (select from list or type in the name)')

	def __init__(self, *args, **kwargs):
		super(EventBase, self).__init__(*args, **kwargs)
		if hasattr(self, 'schools'):
			self.schools.queryset = user_dans()


AddEventForm = model_form( Event, 
	base_class=EventBase, 
	exclude=(
		'end',
		'updated',
		'created',
		'creator',
		'schools',
		'title',
		'description',
		'short_description',
		'places'))


EventForm = model_form(Event, 
	base_class=EventBase, 
	exclude=('updated','created','creator','places'))

