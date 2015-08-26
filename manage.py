from flask.ext.script import Manager, Server

from app import create_app
from app.mod_user import manager as user_manager
from app.mod_dan import manager as dan_manager
from app.mod_proposal import manager as proposal_manager
from app.mod_collection import manager as collection_manager
from app.mod_event import manager as event_manager
from app.mod_discussion import manager as discussion_manager
from app.mod_school import manager as school_manager

# create the manager so decorators work
manager = Manager(create_app())
manager.add_command("runserver", Server(host='0.0.0.0'))
manager.add_command("user", user_manager)
manager.add_command("dan", dan_manager)
manager.add_command("proposal", proposal_manager)
manager.add_command("collection", collection_manager)
manager.add_command("event", event_manager)
manager.add_command("discussion", discussion_manager)
manager.add_command("school", school_manager)


if __name__ == "__main__":
	manager.run()
