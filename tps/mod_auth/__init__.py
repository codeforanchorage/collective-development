from flask.ext.login import LoginManager
from tps.mod_user import User, AnonymousUser

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.refresh_view = 'auth.reauth'
login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(id):
	try:
		return User.objects.get(id=id)
	except:
		return None


def authenticate_user(login, password):
	return User.authenticate(login, password)


# Import views after function definitions
from .views import auth
