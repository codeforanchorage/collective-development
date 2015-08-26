from wtforms import TextField, TextAreaField, BooleanField, SubmitField, HiddenField, SelectMultipleField
from wtforms.validators import Required
from flask.ext.login import current_user

from app.utils.form import model_form, BaseForm, TagListField
from app.mod_school import user_schools
from .models import Comment, Discussion


class DiscussionBase(BaseForm):
	""" Form for starting a discussion """
	text = TextAreaField('Text', [Required()])
	field_order = ('*', 'text', 'submit')

	def __init__(self, *args, **kwargs):
		super(DiscussionBase, self).__init__(*args, **kwargs)
		if hasattr(self, 'schools'):
			self.schools.queryset = user_schools()


class CommentBase(BaseForm):
	""" Form for a comment """
	field_order = ('*', 'submit')


AddDiscussionForm = model_form( Discussion,
	base_class=DiscussionBase,
	exclude=(
		'schools',
		'published',
		'updated',
		'created',
		'creator',
		'priority',
		'num_comments',
		'first_comment',
		'last_comment',
		'last_comment_time'))
submit_add = SubmitField('Start Discussion')
AddDiscussionForm.submit = submit_add


AddCommentForm = model_form( Comment,
	base_class=CommentBase,
	exclude=(
		'published',
		'updated',
		'created',
		'creator',
		'discussion'))
submit_add = SubmitField('Comment')
AddCommentForm.submit = submit_add
