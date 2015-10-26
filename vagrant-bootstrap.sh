#!/bin/bash

# Install MongoDB
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo "deb http://repo.mongodb.org/apt/ubuntu "$(lsb_release -sc)"/mongodb-org/3.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# Install pip, git, virtualenv
sudo apt-get install -y python-pip
sudo apt-get install -y python-virtualenv
sudo apt-get install -y git

# Install numpy dependencies
sudo apt-get install -y python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose 

# Put Code on VM
cd /home/vagrant && git clone https://github.com/codeforanchorage/collective-development.git
