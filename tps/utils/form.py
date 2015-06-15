from dateutil import parser
from flask.ext.mongoengine.wtf.orm import converts, ModelConverter, ModelForm, model_form as orig_model_form
from flask.ext.wtf import Form
from wtforms import fields as f, widgets, HiddenField
from wtforms.fields import Field
from wtforms.widgets import TextInput
from wtforms.ext.dateutil.fields import DateTimeField


class TPSModelConverter(ModelConverter):
	""" Use updated datetime field """
	@converts('DateTimeField')
	def conv_DateTime(self, model, field, kwargs):
		return DateTimeField(**kwargs)


class BaseForm(Form):
	""" This base form allows for re-ordering fields in the form """	
	csrf_enabled=True
	next = HiddenField()
	
	def __iter__(self):
		field_order = getattr(self, 'field_order', None)
		# everything before the wildcard
		if field_order:
			for name in field_order:
				if name=='*':
					break
				elif name in self._fields:
					yield self._fields[name]
		# the wildcard (or field_order not set)
		for k, v in self._fields.iteritems():
			if field_order:
				if k not in field_order:
					yield v
			else:
				yield v
		# everything after the wildcard
		if field_order:
			start = False
			for name in field_order:
				if start and name in self._fields:
					yield self._fields[name]
				if name=='*':
					start = True


class TagListField(Field):
	widget = TextInput()

	def _value(self):
		if self.data:
			return u', '.join(self.data)
		else:
			return u''

	def process_formdata(self, valuelist):
		if valuelist:
			self.data = [x.strip() for x in valuelist[0].split(',')]
		else:
			self.data = []


def model_form(model, base_class=ModelForm, only=None, exclude=None, field_args=None, converter=TPSModelConverter()):
	""" Default to using our custom model converter """
	return orig_model_form(model, base_class=base_class, only=only, exclude=exclude, field_args=field_args, converter=converter)
	