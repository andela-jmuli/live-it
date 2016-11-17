
# live-it

[![Build Status](https://travis-ci.org/andela-jmuli/live-it.svg?branch=bucketlists-endpoints)](https://travis-ci.org/andela-jmuli/live-it)
[![Coverage Status](https://coveralls.io/repos/github/andela-jmuli/live-it/badge.svg?branch=users-v0.1)](https://coveralls.io/github/andela-jmuli/live-it?branch=users-v0.1)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()
## Introduction:
live-it is a bucket list RESTful API that allows creating and editing of bucket lists -- These are a number of experiences or achievements that a person hopes to have or accomplish during their lifetime.  
A quick demo can be viewed [here](https://www.youtube.com/watch?v=xpzk1bfH6eM&feature=youtu.be)

## Dependencies:

1. [Flask](http://flask.pocoo.org/)
2. [Flask-SQLAlchemy]()
3. [Python 2.7](https://www.python.org/)  
4. [flask_httpauth](https://flask-httpauth.readthedocs.io/en/latest/)  
5. [flask_restful](http://flask-restful-cn.readthedocs.io/en/0.3.5/)  
6. [flask_testing](http://flask.pocoo.org/docs/0.11/testing/)

## Installation and Setup:

* Navigate to your directory choice
* Clone the repository:
 * Using SSH:  
    ``` git@github.com:andela-jmuli/live-it.git ```

 * Using HTTP  
    ``` https://github.com/andela-jmuli/live-it.git ```
* Setup a virtualenvironment for dependencies:
    * virtualenv {{ desired name }}
    * Activate your environment
* ``` cd ``` into folder and run ``` source bin/activate ``` to activate the virtual environment
* Install the dependencies:
    * ``` pip install -r reqiuirements.txt ```

* ```cd ``` back to the project root

* Setup the database tables and migrations:  

    * python manage.py db init
    * python manage.py db migrate
    * python manage.py db upgrade

* Run the server via:
    * python manage.py runserver

* you may user Chrome's extension [Postman](https://www.getpostman.com/) to view or use api

## Usage:  
#### Endpoints  


| Tables        | Are           | Requires Authentication |
| ------------- |:-------------:| -------------:|
| POST auth/login    | Log a user in | False |
| POST auth/register     | Register a new user | False |
| POST /bucketlists/ | Create a new bucketlist   | True |
| GET /bucketlists/      | List all created bucketlists | True |
| GET /bucketlists/id     | get single bucketlist | True |
| PUT /bucketlists/id | update single bucketlist | True |
| DELETE bucketlists/id      | Delete a single bucketlist | True |
| POST bucketlists/id/items/      | Create a new item in a bucketlist | True |
| PUT bucketlists/id/items/item_id | Update an item in a bucketlist | True |
| DELETE bucketlists/id/items/item_id      | Delete an item in a bucketlist | True |

#### Use Cases:

**Registering a new user:**  
Ensure the URL points to http://localhost:5000/api/v1/auth/register/ as a POST request:  
This is a parameterized request thus you need to provide a name and password

![Alt text](/source/registe_new_user.png?raw=true "Optional Title") .

**Authenticating a user (Login)**
Ensure the URL points to http://localhost:5000/api/v1/auth/login/ as a POST request:  
This is a parameterized request thus you need to provide a name and password

![Alt text](/source/login_users.png?raw=true "Optional Title")

**Creating a Bucketlist:**
Ensure the URL points to http://localhost:5000/api/v1/bucketlists/ as a POST request.
This is a parameterized request thus you need to provide a name and optionally description
This is also a secure request thus make sure you include the token as a header during this request as below:  
The key should be Authorization and the value should be prefixed with Token then [token]: i.e.  
``` Authorization : Token sdvbjsdvnskdvna;scma;scma;cfskvbjrv ```  

![Alt text](/source/create_bucketlist.png?raw=true "Optional Title")

**Listing all bucketlists:**  
Ensure the URL points to http://localhost:5000/api/v1/bucketlists/ as a GET request.  
This is also a secure request thus make sure you include the token as a header during this request.  

![Alt text](/source/list_all_bucketlists.png?raw=true "Optional Title")

**Creating a bucketlist item:**  
Ensure the URL points to http://localhost:5000/api/v1/bucketlists/bucketlist_id/items as a POST request.
You have to ensure you have a bucketlist in order to create an item in it.
This is also a parameterized request thus you need to provide an item name and optionally description
This is also a secure request thus make sure you include the token as a header during this request.

![Alt text](/source/create_bucketlist_item.png?raw=true "Optional Title")

**Listing all bucketlists with items:**  
Ensure the URL points to http://localhost:5000/api/v1/bucketlists/ as a GET request.  
This is also a secure request thus make sure you include the token as a header during this request

![Alt text](/source/list_all_bucketlists.png?raw=true "Optional Title")

## Testing:  
 To test, run the command tox

## Licence:
Check out the License file for more information

## Credits:
* [Joseph Muli](github.com/andela-jmuli)
