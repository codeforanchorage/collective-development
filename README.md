Collective Development
======================

# Development Quickstart

Local development can be done with Vagrant or Docker. Instructions for both below.

## Vagrant

Vagrant requires that you download [Virtualbox](https://www.virtualbox.org/wiki/Downloads) and [Vagrant](https://www.vagrantup.com/downloads.html)

Once you have those installed, `git clone` this code and start vagrant:

```
git clone https://github.com/codeforanchorage/collective-development.git
cd collective-development
vagrant up
```

Wait for this to load, it will take some time. Once it is finished, get onto the vagrant VM:
```
vagrant ssh 
cd collective-development
sudo virtualenv venv
source venv/bin/activate
sudo pip install -r requirements.txt
```

This last step will take some time too.

### Create Fake Data and start the server

Run:
```
python manage.py fake_data
```

You can read more details in the section 'Before starting the server'

Start the server:
```
python wsgi.py
```

And go to http://192.168.61.2:5000


## Docker

```
$ docker-compose start # builds and launches mongodb and application server
$ docker-compose run web python manage.py fake_data # populates db with fake data
```

### Pre-installation

1. Install MongoDB (instructions for OSX are [http://docs.mongodb.org/manual/tutorial/install-mongodb-on-os-x/](here))
and make sure it is running

2. Make sure pip is installed (for OSX: "sudo easy_install pip")

3. Make sure virtualenv is installed. If not: "pip install virtualenv"

### Installation

```
git clone https://github.com/codeforanchorage/collective-development.git
cd collective-development
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Before starting the server

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


### Starting the server

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

## Issues

Issues that you may run into as you do the install, especially if you do a raw install without Docker or Vagrant:

### MongoDB does not start

Make sure the mongo daemon is running:

```
tail /var/log/mongodb/mongod.log
```
Look for a line reading
```
[initandlisten] waiting for connections on port 27017
```
If it isn't running, start the service:
```
sudo service mongod start
```


Mongo requires a very large journal file directory (>3GB). If you see a line in mongod.log such as
```
[initandlisten] Insufficient free space for journal files
```
allocate more space to the volume containing /var/lib/mongodb/journal and try again.

### Python syntax errors during pip install

If you are installing on Ubuntu 14.04 LTS, for example, you may not have Python 2.7 installed. Install 2.7 and try again.

(For Ubuntu)
```
sudo apt-get update
sudo apt-get install python2.7-dev
```
