Collective Development
======================

# Development Quickstart

```
$ docker-compose start # builds and launches mongodb and application server
$ docker-compose run web python manage.py fake_data # populates db with fake data
```

# Pre-installation

1. Install MongoDB (instructions for OSX are [http://docs.mongodb.org/manual/tutorial/install-mongodb-on-os-x/](here))
and make sure it is running

2. Make sure pip is installed (for OSX: "sudo easy_install pip")

3. Make sure virtualenv is installed. If not: "pip install virtualenv"

# Installation

```
git clone https://github.com/codeforanchorage/collective-development.git
cd collective-development
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Before starting the server

Before starting the server, you need some data. Run the following command:

```python
python manage.py fake_data
```
which creates:

- admin with name "collectivedevelopment" and password "collectivedevelopment"
- 4 schools
- 25 users
- 40 proposals
- 10 places
- 10 events
- 30 discussions


# Starting the server

At this point, you can start the server and play around. That is simply:

```
python wsgi.py
```

Now visit http://localhost:5000/


# Configuring things

If you need to delete all the users, places, events, or proposals, do the following:

```
python manage.py event delete_events
python manage.py event delete_places
python manage.py proposal delete_all
python manage.py user delete_all
```

You will probably have noticed that the development server is already running in "multi-school" mode. (Each school is run as its own application, but they all share the same database. More on this later, but for now, if you want to add more schools, simply add to the list in _wsgi.py_!) You can add a user to the committee for a school by doing, for example:

```
python manage.py dan add_user -u sdockray -s la
```

and then the following commands to remove a user or clear out all committees

```
python manage.py dan remove_user -u username -s schoolname
python manage.py dan delete_all
```
