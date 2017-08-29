[![Build Status](https://travis-ci.org/Annettesunday/BUCKETLIST-FLASK-API.svg?branch=develop)](https://travis-ci.org/Annettesunday/BUCKETLIST-FLASK-API) [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) [![Coverage Status](https://coveralls.io/repos/github/Annettesunday/BUCKETLIST-FLASK-API/badge.svg?branch=develop)](https://coveralls.io/github/Annettesunday/BUCKETLIST-FLASK-API?branch=develop) [![Code Health](https://landscape.io/github/Annettesunday/BUCKETLIST-FLASK-API/develop/landscape.svg?style=flat)](https://landscape.io/github/Annettesunday/BUCKETLIST-FLASK-API/develop)
Introduction

What would you like to do in the next few years? Climb a mountain? Learn to ride a bike? :) It’s important to keep track of what you have already done and what you are yet to achieve. Register and start tracking.

Features

User should be able to register and login

User should be able to create a Bucketlist

User should be able to add itemsto a bucketlist

User should be able to edit and delete bucketlists

User should be able to edit and delete bucketlist items


Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Prerequisites

Python 2.7 Comes inbuilt for unix but can also be downloaded from Python downloads
Installing

Clone this repo from github by running: with ssh:

$ git clone git@github.com:Annettesunday/BUCKETLIST-FLASK-API
with http:

$ git clone https://github.com/Annettesunday/BUCKETLIST-FLASK-API.git
Set up a virtual environment for the project and install the dependencies

$ mkvirtualenv amity
$ pip install -r requirements.txt
Running the project locally

Create a .env file in the root directory and save it. It should contain your secret key stored under the variable SECRET_KEY which will be used to secure your data.

Innitialize the database

$ python manage.py db init
Create migrations folder

$ python manage.py db migrate
Migrate the migrations to the database

$ python manage.py db upgrade


URL endpoints

The following endpoints are provided

URL Endpoint	HTTP Methods	Summary
/auth/register	POST	Register a new user
/auth/login	POST	Login and retrieve token
/bucketlist	POST	Create a new Bucketlist
/bucketlist	GET	Retrieve all bucketlists for user
/bucketlists/?q=bucket	GET	Match bucketlist by name
/bucketlists/<id>	GET	Retrieve bucket list details
/bucketlists/<id>	PUT	Update bucket list details
/bucketlists/<id>	DELETE	Delete a bucket list
/bucketlists/<id>/items	POST	Create items in a bucket list
/bucketlists/<id>/items/<item_id>	DELETE	Delete a item in a bucket list
/bucketlists/<id>/items/<item_id>	PUT	update a bucket list item details
Running the tests

 They can be run by the command

python manage.py test

The tests make use of HTTP response codes to ensure users are getting the expected responses from the api as well as token based authentication which ensures security of users data by ensuring only authorised users gain access to sensitive data.

Built With

Python - A verstile programming language
Flask - A multipurpose python web framework
Contributing

Contributions are open, fork the repository and make a pull requestwith the changes which will be reviewed before merging on approval.

Authors

Annette Sunday- Initial work - Annette Sunday
License

This project is licensed under the MIT License - see the LICENSE file for details

Acknowledgments

Several Andela Fellows consulted during development
Facilitators