from flask.ext.script import Manager

from tps import create_app
from tps.mod_user import manager as user_manager
from tps.mod_dan import manager as dan_manager
from tps.mod_proposal import manager as proposal_manager
from tps.mod_event import manager as event_manager
from tps.mod_school import manager as school_manager

# create the manager so decorators work
manager = Manager(create_app())
manager.add_command("user", user_manager)
manager.add_command("dan", dan_manager)
manager.add_command("proposal", proposal_manager)
manager.add_command("event", event_manager)
manager.add_command("school", school_manager)


if __name__ == "__main__":
	manager.run()