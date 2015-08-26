"""
A Collection is a way of aggregating proposals, events, resources, discussions.
"""
import datetime
import operator

from bson import ObjectId
from mongoengine import CASCADE, NULLIFY

from app.utils import pretty_date
from app.database import db
from app.mod_user import User
from app.mod_interest import Interested
from app.mod_school import School
from app.mod_proposal import Proposal, BaseProposal
from app.mod_event import Event


class Collection(BaseProposal):
	""" A collection object """

	meta = {'collection': 'app_collection'}
	# directly included proposals
	proposals = db.ListField(db.ReferenceField(Proposal))
	collections = db.ListField(db.ReferenceField('self'))
	# todo: url


	def __init__(self, *args, **kwargs):
		super(Collection, self).__init__(*args, **kwargs)
		if not self.id:
			self.interested.append(Interested(user=self.proposer))
			self.num_interested = 1


	def add_proposal(self, p):
		self.update(add_to_set__proposals=p)
		self.reload()


	def remove_proposal(self, p):
		self.update(pull__proposals=p)
		self.reload()


	def add_collection(self, c):
		self.update(add_to_set__collections=c)
		self.reload()


	def remove_collection(self, c):
		self.update(pull__collections=c)
		self.reload()


	def all_proposals(self):
		''' Gets all events, including those from enclosed proposals and collections '''
		all_proposals = {}
		for c in self.collections:
			all_proposals.update(c.all_proposals())
		for p in self.proposals:
			all_proposals[p.id] = p
		return sorted(all_proposals.values(), key=operator.attrgetter('title'))


	def all_events(self, date_sorted=True):
		''' Gets all events, including those from enclosed proposals and collections '''
		all_events = {}
		for c in self.collections:
			all_events.update(c.all_events())
		for p in self.proposals:
			for e in p.events:
				all_events[e.id] = e
		for e in self.events:
			all_events[e.id] = e
		if date_sorted:
			return sorted(all_events.values(), key=operator.attrgetter('start'))
		else:
			return all_events
