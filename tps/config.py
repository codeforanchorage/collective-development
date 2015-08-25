import os


class base_config(object):
	SITE_NAME = 'The Public School'
	SERVER_NAME = os.environ.get('SERVER_NAME')
	SECRET_KEY = os.environ.get('SECRET_KEY','secrets')
	MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
	MAIL_PORT = os.environ.get('MAIL_PORT', 1025)
	DEFAULT_SCHOOL = 'www' # In "single-school" mode, or the root within "multi-school" mode
	MONGODB_SETTINGS = {
		'db': 'tps',
		'host': os.environ.get('DB_PORT_27017_TCP_ADDR'),
		'port': int(os.environ.get('DB_PORT_27017_TCP_PORT')),
	}
	ACCEPT_LANGUAGES = ['zh']
	BABEL_DEFAULT_LOCALE = 'en'


class dev_config(base_config):
	DEBUG = True
	ASSETS_DEBUG = True


class test_config(base_config):
	TESTING = True
	WTF_CSRF_ENABLED = False
