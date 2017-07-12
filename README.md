# bucketlist_API
[![Build Status](https://travis-ci.org/Andretalik/bucketlist_API.svg?branch=develop)](https://travis-ci.org/Andretalik/bucketlist_API)
[![Coverage Status](https://coveralls.io/repos/github/Andretalik/bucketlist_API/badge.svg?branch=develop)](https://coveralls.io/github/Andretalik/bucketlist_API?branch=develop)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/c71a08db463f4c27a6bab5cbb4485c2b/badge.svg)](https://www.quantifiedcode.com/app/project/c71a08db463f4c27a6bab5cbb4485c2b)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/9c58fe1b36a7436c847c014894a49d44)](https://www.codacy.com/app/Andretalik/bucketlist_API?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Andretalik/bucketlist_API&amp;utm_campaign=Badge_Grade)


By definition, a bucket-list is a list of things that an individual wants to do before a certain time.
This repository has been written in Flask to achieve exactly that. It is an API that allows a registered user to create a bucket-list, populate the bucket-list with the list of things that they want to have done before a specific point in time, as well as mark their progress.
### The Endpoints

The bucketlist API has the following endpoints

| Endpoint | Functionality |
| -------- | ------------- |
| POST /auth/login | Logs a user in |
| POST /auth/register | Register a user |
| POST /bucketlists | Create a new bucket list |
| GET /bucketlists	| List all the created bucket lists |
| GET /bucketlists/<id> | Get single bucket list |
| PUT /bucketlists/<id> | Update this bucket list |
| DELETE /bucketlists/<id> | Delete this single bucket list |
| GET /bucketlists/<id>/items/<item_id> | Get a single bucket list item |
| POST /bucketlists/<id>/items | Create a new item in bucket list |
| PUT /bucketlists/<id>/items/<item_id> | Update a bucket list item |
| DELETE /bucketlists/<id>/items/<item_id> | Delete an item in a bucket list |



### Installation
Clone the repository.

Navigate into the repo root and checkout to the master branch.

Create an isolated virtual environment.

Install the dependencies:
```python
pip install -r requirements.txt.
```

create a .env file and add the following.

```sh
source workon "isolated environment name"
export FLASK_APP="run.py"
export SECRET="you-should-make-it-as-SECRET-as-possible"
export APP_SETTINGS="development"
```
### Setup Up Database And Migrations
Run the migrations to correctly setup the database.

```python
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
Flask Run
```

When you run the server it should print out:
```
Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Testing
To run the tests:
```
nosetests --with-coverage
```
This will return the number of tests that were run as well as the coverage.

Author
----
	-Adrian Andre Adero Otieno
