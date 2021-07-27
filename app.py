import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy, exc
from flask_cors import CORS
# from .database.models import db_drop_and_create_all, setup_db, Drink
# from models import db_drop_and_create_all, setup_db, Actors, Movies
# from .auth.auth import AuthError, requires_auth
from auth import AuthError, requires_auth
from models import setup_db, Movies, Actors

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  return app

APP = create_app()

app = Flask(__name__)
setup_db(app)
CORS(app)


# ROUTES
'''
@TODO implement endpoint
    GET /actors
        it should be a public endpoint
    returns status code 200 and json {"success": True, "actors": actors}
    where actors is the list of actors
        or appropriate status code indicating reason for failure
'''

@app.route('/actors', methods=['GET'])
def display_actors():

    actors = Actors.query.all()

    try:

#        actors = [actor.short() for actor in actors]

        if len(actors) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actors': actors
            }), 200

    except BaseException:
        abort(400)

'''
@TODO implement endpoint
    GET /movies
        it should be a public endpoint
    returns status code 200 and json {"success": True, "movies": movies}
    where movies is the list of movies
        or appropriate status code indicating reason for failure
'''

@app.route('/movies', methods=['GET'])
def display_movies():

    movies = Movies.query.all()

    try:

#        movies = [movie.short() for movie in movies]

        if len(movies) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'movies': movies
            }), 200

    except BaseException:
        abort(400)

'''
@TODO implement endpoint
    GET /actors-details
        it should require the 'get:actors-details' permission
    returns status code 200 and json {"success": True, "actors": actors}
     where actors is the list of actors
        or appropriate status code indicating reason for failure
'''
'''
@app.route('/actors-details', methods=['GET'])
@requires_auth('get:actors-details')
def display_actors_details(payload):

    actors = Actors.query.order_by(Actors.id).all()
    try:

#        actors = [actor.long() for actor in actors]

        if len(actors) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actors': actors
            }), 200

    except BaseException:
        abort(400)
'''

'''
@TODO implement endpoint
    GET /movies-details
        it should require the 'get:movies-details' permission
    returns status code 200 and json {"success": True, "movies": movies}
     where movies is the list of movies
        or appropriate status code indicating reason for failure
'''

'''
@app.route('/movies-details', methods=['GET'])
@requires_auth('get:movies-details')
def display_movies_details(payload):

    movies = Movies.query.order_by(Movies.id).all()
    try:

#        movies = [movie.long() for movie in movies]

        if len(movies) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'movies': movies
            }), 200

    except BaseException:
        abort(400)
'''

'''
@TODO implement endpoint
    POST /actors
        it should create a new row in the actors table
        it should require the 'post:actors' permission
    returns status code 200 and json {"success": True, "actors": actor}
     where actor an array containing only the newly created actor
        or appropriate status code indicating reason for failure
'''

@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def create_actors(payload):

    new_name = request.json.get('name', None)
    new_age = request.json.get('age', None)
    new_gender = request.json.get('gender', None)

    if new_name is None:
        abort(422)
    if new_age is None:
        abort(422)
    if new_gender is None:
        abort(422)

    actors = Actors(name=new_name, age=new_age, gender=new_gender)
    actors.insert()

    return jsonify({
        'success': True,
#         'actors': [actors.long()]
    }), 200


'''
@TODO implement endpoint
    POST /movies
        it should create a new row in the movies table
        it should require the 'post:movies' permission
    returns status code 200 and json {"success": True, "movies:movie}
     where movie an array containing only the newly created movie
        or appropriate status code indicating reason for failure
'''

@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def create_movies(payload):

    new_title = request.json.get('title', None)
    new_release_date = request.json.get('release_date', None)

    if new_title is None:
        abort(422)
    if new_release_date is None:
        abort(422)

    movies = Movies(title=new_title, release_date=new_release_date)
    movies.insert()

    return jsonify({
        'success': True,
#         'movies': [movies.long()]
    }), 200


'''
@TODO implement endpoint
    PATCH /actors/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:actors' permission
    returns status code 200 and json {"success": True, "actors": actor}
     where actor an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def modify_actors(payload, id):

    body = request.get_json()
    actors = Actors.query.filter(Actors.id == id).one_or_none()
    old_name = Actors.name
    old_age = Actors.age
    old_gender = Actors.gender

    if actors is None:
        abort(404)
    else:
        try:
            if 'name' in body:
                actors.name = body.get('name')
            else:
                actors.name = old_name
            if 'age' in body:
                actors.age = body.get('age')
            else:
                actors.age = old_age
            if 'gender' in body:
                actors.gender = body.get('gender')
            else:
                actors.gender = old_gender

            actors.update()

            return jsonify({
                'success': True,
#                 'actors': [actors.long()]
            })
        except BaseException:
            abort(400)


'''
@TODO implement endpoint
    PATCH /movies/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:movies' permission
    returns status code 200 and json {"success": True, "movies": movie}
     where movie an array containing only the updated movie
        or appropriate status code indicating reason for failure
'''

@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def modify_movies(payload, id):
    
    body = request.get_json()
    movies = Movies.query.filter(Movies.id == id).one_or_none()
    old_title = Movies.title
    old_release_date = Movies.release_date

    if movies is None:
        abort(404)
    else:
        try:
            if 'title' in body:
                movies.title = body.get('title')
            else:
                movies.title = old_title
            if 'release_date' in body:
                movies.release_date = body.get('release_Date')
            else:
                movies.release_date = old_release_date

            movies.update()

            return jsonify({
                'success': True,
#                 'movies': [movies.long()]
            })
        except BaseException:
            abort(400)


'''
@TODO implement endpoint
    DELETE /actors/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:actors' permission
    returns status code 200 and json {"success": True, "delete": id}
     where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actors(payload, id):

    try:
        actors = Actors.query.filter(Actors.id == id).one_or_none()

        if actors is None:
            abort(404)
        else:
            actors.delete()
            return jsonify({
                'success': True,
                'delete': actors.id,
            })

    except BaseException:
        abort(422)

'''
@TODO implement endpoint
    DELETE /movies/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:movies' permission
    returns status code 200 and json {"success": True, "delete": id}
     where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movies(payload, id):

    try:
        movies = Movies.query.filter(Movies.id == id).one_or_none()

        if movies is None:
            abort(404)
        else:
            movies.delete()
            return jsonify({
                'success': True,
                'delete': movies.id,
            })

    except BaseException:
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)