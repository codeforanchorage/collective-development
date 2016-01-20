from flask import Blueprint, g, current_app, render_template, flash, redirect, request, url_for, jsonify, Markup
from flask.ext.login import current_user, login_required
from flask.ext.babel import gettext as _

from .services import add_user_interest, remove_user_interest

# Blueprint definition
interested = Blueprint('interested', __name__, url_prefix='/interested')


@interested.route('/<type>/<id>', methods=['POST'])
def toggle(type, id):
    if current_user.is_anonymous():
        return jsonify({'anon':True})
    """ Toggles current user's interest in a proposal """
    from app.mod_proposal import Proposal
    from app.mod_event import Event

    u = current_user._get_current_object()
    remove = request.form.get('action','add')=='remove'
    attribute = request.form.get('attribute', None) or None
    if type=='event':
        cls = Event
    else:
        cls = Proposal
    # Now try and load the document
    obj = cls.objects.get_or_404(id=id)
    # Do the adding or removing
    if remove:
        remove_user_interest(u, obj, cls, only=attribute)
    else:
        add_user_interest(u, obj, cls, extra=attribute)

	# Used for updating the list of interested users
    interested_users = []
    for user in obj.interested_users:
        interested_users.append(user.display_name)

    return jsonify({
		'num_interested':obj.num_interested,
		'next' : 'remove' if obj.user_is_interested(u) else 'add',
        'interested_users':interested_users
		})
