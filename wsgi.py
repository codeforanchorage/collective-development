from werkzeug.serving import run_simple
from werkzeug.wsgi import DispatcherMiddleware

from tps import create_app


if __name__ == "__main__":
	""" 
	In local development environment, multiple schools are simulated as below.
	In production, the app will be run under uwsgi and SCRIPT_NAME will be set in
	the wsgi variables. Each school will be its own script: http://domain.net/school
	"""
	# List every school here
	schools = ['la','berlin','brussels']
	apps = {}
	app = create_app()
	for school in schools:
		apps['/'+school] = create_app(school_name=school)
	# now create all the app instances
	master_app = DispatcherMiddleware(app, apps)
	run_simple('localhost', 5000, master_app, use_reloader=True)
