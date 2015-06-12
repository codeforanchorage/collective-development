from wtforms import TextField, TextAreaField, BooleanField, SubmitField, HiddenField
from wtforms.validators import Required
#from flask.ext.mongoengine.wtf import model_form

from tps.utils.form import model_form, BaseForm, TagListField
from .models import Proposal


class ProposalBase(BaseForm):
	""" Full event form """
	tags = TagListField('Tags (comma separated)')
	field_order = ('*', 'tags', 'submit')


AddProposalForm = model_form( Proposal, 
	base_class=ProposalBase, 
	exclude=(
		'edited_description',
		'proposer',
		'schools',
		'published',
		'stage',
		'source',
		'updated',
		'created',
		'interested',
		'num_interested',
		'copy_of',
		'tags'))
submit_add = SubmitField('Propose!')
AddProposalForm.submit = submit_add


ProposalForm = model_form( Proposal, 
	base_class=ProposalBase, 
	exclude=(
		'edited_description',
		'proposer',
		'schools',
		'published',
		'stage',
		'source',
		'updated',
		'created',
		'interested',
		'num_interested',
		'copy_of',
		'tags'))
submit_save = SubmitField('Save')
ProposalForm.submit = submit_save


