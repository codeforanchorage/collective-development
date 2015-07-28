from random import randint

from flask import g, abort
from flask.ext.login import current_user
from tps.mod_dan import load_dan, user_is_a_dan
from .models import Collection


def random_collection():
	""" Gets a random collection """
	count = Collection.objects.count()
	return Collection.objects.limit(-1).skip(randint(0,count-1)).next()


def delete_all_collections():
	""" Deletes all the proposals. Careful! """
	Collection.drop_collection()