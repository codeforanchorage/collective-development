from wtforms import SubmitField
from app.utils.form import model_form, BaseForm
from .models import School

class SchoolBase(BaseForm):
	""" Form for a comment """
	field_order = ('*', 'submit')

SchoolForm = model_form( School,
	base_class=SchoolBase)
submit_add = SubmitField('Add School')
SchoolForm.submit = submit_add