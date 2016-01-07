from random import randint

from flask import g, abort
from flask.ext.login import current_user
from app.mod_dan import load_dan, user_is_a_dan
from .models import Discussion, Comment


def start_discussion(text, title=None, schools=None, form=None):
	""" Starts a discussion with some comment text """
	if not schools:
		schools = [g.school,]
	if title:
		d = Discussion(
			title=title,
			schools=schools,
			creator=current_user._get_current_object())
	elif form:
		d = Discussion(
			schools=schools,
			creator=current_user._get_current_object())
		if form:
			form.populate_obj(d)
	else:
		return None
	d.save()
	c = Comment(
		text = text,
		creator = current_user._get_current_object(),
		discussion = d)
	c.save()
	return d


def add_comment(text, user, discussion, time=None):
	""" Adds a comment with text by user to a discussion """
	discussion.add_comment(text, user, time=time)


def random_discussion():
	""" Gets a random discussion """
	count = Discussion.objects.count()
	return Discussion.objects.limit(-1).skip(randint(0,count-1)).next()


def delete_all_discussions():
	""" Deletes all the discussions. Careful! """
	Comment.drop_collection()
	Discussion.drop_collection()

def can_edit_comment(comment):
	""" Can a user edit a particular comment of a proposal?
	Allow the comment author """
	return comment.creator == current_user._get_current_object()