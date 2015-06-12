from wtforms import TextField, BooleanField, SubmitField, HiddenField
from wtforms.validators import Required
#from flask.ext.mongoengine.wtf import model_form

from tps.utils.form import model_form, BaseForm
from .models import Event


class EventBase(BaseForm):
	""" Full event form """
	submit = SubmitField('Save')
	field_order = ('*', 'submit')


AddEventForm = model_form( Event, 
	base_class=EventBase, 
	exclude=('end','updated','created','proposals','creator','schools','title','description','short_description','places'))


EventForm = model_form(Event, 
	base_class=EventBase, 
	exclude=('updated','created','proposals','creator','schools'))

