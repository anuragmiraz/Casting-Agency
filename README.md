# Full Stack - Casting Agency project

This project is the final project for my Udacity FullStack Developer Nanodegree.
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

Roles:

1. Casting Assistant
Can view actors and movies

2. Casting Director
All permissions a Casting Assistant has and…
Add or delete an actor from the database
Modify actors or movies

3. Executive Producer
All permissions a Casting Director has and…
Add or delete a movie from the database

This Application does not have a frontend implemented. It is a server only application at the moment.

To run this application, please follow below steps.

### Step 1 - Installing Dependencies

Install the below dependencies (possibly the latest verison) by putting them in a requirements.txt file. 

alembic==1.5.8
aniso8601==6.0.0
appdirs==1.4.4
astroid==2.2.5
atomicwrites==1.4.0
attrs==21.2.0
autopep8==1.5.7
awscli==1.19.111
Babel==2.9.0
bcrypt==3.2.0
botocore==1.20.111
cffi==1.14.5
Click==7.0
colorama==0.4.3
cryptography==3.4.7
distlib==0.3.1
docutils==0.15.2
ecdsa==0.13.2
filelock==3.0.12
Flask==1.1.2
Flask-Cors==3.0.8
Flask-Migrate==2.7.0
Flask-Moment==0.11.0
Flask-RESTful==0.3.7
Flask-Script==2.0.6
Flask-SQLAlchemy==2.4.0
Flask-WTF==0.14.3
future==0.17.1
greenlet==1.0.0
gunicorn==20.0.4
iniconfig==1.1.1
isort==4.3.18
itsdangerous==1.1.0
Jinja2==2.10.1
jmespath==0.10.0
jwt==1.2.0
lazy-object-proxy==1.4.0
Mako==1.1.4
MarkupSafe==1.1.1
mccabe==0.6.1
packaging==21.0
pluggy==0.13.1
postgres==3.0.0
psycopg2==2.8.6
psycopg2-binary==2.8.6
psycopg2-pool==1.1
py==1.10.0
pyasn1==0.4.8
pycodestyle==2.7.0
pycparser==2.20
pycryptodome==3.3.1
pycryptodomex==3.10.1
pylint==2.3.1
pyparsing==2.4.7
pytest==6.2.2
python-dateutil==2.6.0
python-dotenv==0.17.1
python-editor==1.0.4
python-jose==3.2.0
python-jose-cryptodome==1.3.2
pytz==2019.1
PyYAML==5.4.1
rsa==4.7.2
s3transfer==0.4.2
six==1.12.0
SQLAlchemy==1.3.4
toml==0.10.2
typed-ast==1.4.2
urllib3==1.26.6
virtualenv==20.4.3
Werkzeug==2.0.1
wrapt==1.11.1
WTForms==2.3.3

Install these dependencies by naviging to the directory and running:
pip install -r requirements.txt

This will install all of the required packages we selected within the `requirements.txt` file.

### Step 2 - Database Setup

You need to install and start postgres database.

You need to update the database_params variable found in .env file as shown below:
DATABASE_HOST=localhost:5432
DATABASE_NAME=casting_agency
DATABASE_USER=postgres
DATABASE_PASSWORD=YOUR DB PASSWORD

Note: you can create a db named casting_agency by using createdb command as shown below:

createdb -U postgres casting_agency

### Step 3 - Running the server

For Windows users, use below commands to run the server - 

Login to you project folder. From there to run the server, execute below in sequence:

set FLASK_APP=manage.py
set FLASK_DEBUG=True
python -m flask run

The application will run on http://127.0.0.1:5000/ by default and is a proxy in the frontend configuration.

Heroku address: https://anuragmiraz.herokuapp.com/

### Step 4 - Authentication and authorization

This API uses Auth0 for authentication, you will need to setup Auth0 application and API. You will need to update auth0_params variable found in .env.


## Tests
You can run the unit test cases that are defined in test_app.py using the below command:

python test_app.py


## Error Handling
Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}

The API will return below error types when requests fail:

400: Bad Request
404: Resource Not Found
422: Not Processable
401, 403: Authorisation / security token related errors


## Endpoints

GET /actors
- Fetches a dictionary of actors in which the keys are the ids and the value is the corresponding string of the category
- Security enabled: None
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: actor_string key:value pairs. 
{
    "actors": [
        {
            "age": 3,
            "gender": "M",
            "id": 1,
            "name": "Anurag"
        },
        {
            "age": 35,
            "gender": "M",
            "id": 4,
            "name": "Ayaansh"
        },
    ],
    "success": true
}


GET /movies
- Fetches a dictionary of movies in which the keys are the ids and the value is the corresponding string of the category
- Security enabled: None
- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: movie_string key:value pairs. 
{
    "movies": [
        {
            "id": 1,
            "release_date": "Mon, 01 Feb 2021 18:30:00 GMT",
            "title": "Test"
        },
        {
            "id": 3,
            "release_date": "Thu, 11 Feb 2021 18:30:00 GMT",
            "title": "Fight"
        }
    ],
    "success": true
}

GET '/actors/${id}'
- Fetches specific actor details
- Security enabled: Yes
- Request Arguments: id - integer
- Returns: An object with actor details 
{
    "actors": [
        {
            "age": 3,
            "gender": "M",
            "id": 1,
            "name": "Anurag"
        },
    ],
    "success": true
}

GET '/movies/${id}'
- Fetches specific movie details
- Security enabled: Yes
- Request Arguments: id - integer
- Returns: An object with movie details 
{
    "movies": [
        {
            "id": 1,
            "release_date": "Mon, 01 Feb 2021 18:30:00 GMT",
            "title": "Test"
        },
    ],
    "success": true
}

POST '/actors'
- Sends a post request in order to create a new actor details 
- Security enabled - Yes
- Request Body: 
{'name':  name of the actor (string)
'age': age of actor (integer) 
'gender': gender of ator (String)}
- Returns: Does not need to return anything besides the appropriate HTTP status code and :
{
    "success": True
} 

POST '/movies'
- Sends a post request in order to create a new movie details 
- Request Body: 
{'title':  title of the movie (string)
'release_date': release date of movie (Date) 
- Returns: Does not need to return anything besides the appropriate HTTP status code and :
{
    "success": True
} 

DELETE '/actors/${id}'
- Deletes a specified actor using the id of the actor
- Security enabled - Yes
- Request Arguments: id - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code and :
{
    "success": True
} 

DELETE '/movies/${id}'
- Deletes a specified movie using the id of the movie
- Security enabled - Yes
- Request Arguments: id - integer
- Returns: Does not need to return anything besides the appropriate HTTP status code and :
{
    "success": True
} 

PATCH '/actors/${id}'
- Updates a specified actor details using the id of the actor
- Security enabled - Yes
- Request Arguments: id - integer, and the field which needs to be updated
- Returns: Does not need to return anything besides the appropriate HTTP status code and :
{
    "success": True
} 

PATCH '/movies/${id}'
- Updates a specified movie details using the id of the movie
- Security enabled - Yes
- Request Arguments: id - integer, and the field which needs to be updated
- Returns: Does not need to return anything besides the appropriate HTTP status code and :
{
    "success": True
} 


## Open Issues

None

## Acknowledgements
I would like to pass my sincere thanks to my mentor Dharini for giving me right guidance whenever i needed. Also, to Udacity team members who really helped me alot in solving my problems and giving  wonderful sessions.