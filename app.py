import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy import exc
from flask_cors import CORS
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

        if len(actors) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actors':[actor.format() for actor in actors]
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

        if len(movies) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'movies':[movie.format() for movie in movies]
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

@app.route('/actors-details/<int:id>', methods=['GET'])
@requires_auth('get:actors-details')
def display_actors_details(payload, id):

    actors = Actors.query.order_by(Actors.id).all()
    try:

        if len(actors) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actors':[actor.format() for actor in actors]
            }), 200

    except BaseException:
        abort(400)

'''
@TODO implement endpoint
    GET /movies-details
        it should require the 'get:movies-details' permission
    returns status code 200 and json {"success": True, "movies": movies}
     where movies is the list of movies
        or appropriate status code indicating reason for failure
'''

@app.route('/movies-details/<int:id>', methods=['GET'])
@requires_auth('get:movies-details')
def display_movies_details(payload, id):

    movies = Movies.query.order_by(Movies.id).all()
    try:

        if len(movies) == 0:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'movies':[movie.format() for movie in movies]
            }), 200

    except BaseException:
        abort(400)

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

    new_name = request.form.get('name', None)
    new_age = request.form.get('age', None)
    new_gender = request.form.get('gender', None)

    print(new_name)

    if new_name is None:
        abort(422)
    if new_age is None:
        abort(422)
    if new_gender is None:
        abort(422)

    actors = Actors(name=new_name, age=new_age, gender=new_gender)
    actors.insert()

    return jsonify({
        'success': True
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

    new_title = request.form.get('title', None)
    new_release_date = request.form.get('release_date', None)

    if new_title is None:
        abort(422)
    if new_release_date is None:
        abort(422)

    movies = Movies(title=new_title, release_date=new_release_date)
    movies.insert()

    return jsonify({
        'success': True
    }), 200


'''
@TODO implement endpoint
    PATCH /actors/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:actors' permission
    returns status code 200 and json {"success": True, "actors": actor}
     where actor an array containing only the updated actor
        or appropriate status code indicating reason for failure
'''

@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def modify_actors(payload, id):

    actors = Actors.query.filter(Actors.id == id).one_or_none()
    old_name = Actors.name
    old_age = Actors.age
    old_gender = Actors.gender

    if actors is None:
        abort(404)
    else:
        try:
            new_name = request.form.get('name', None)
            new_age = request.form.get('age', None)
            new_gender = request.form.get('gender', None)

            if new_name is not None:
                actors.name = new_name
            else:
                actors.name = old_name
            
            if new_age is not None:
                actors.age = new_age
            else:
                actors.age = old_age
            
            if new_gender is not None:
                actors.gender = new_gender
            else:
                actors.gender = old_gender

            actors.update()

            return jsonify({
                'success': True
            }), 200
        except BaseException:
            abort(422)

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
    
    movies = Movies.query.filter(Movies.id == id).one_or_none()
    
    old_title = Movies.title
    old_release_date = Movies.release_date

    if movies is None:
        abort(404)
    else:
        try:

            new_title = request.form.get('title', None)
            new_release_date = request.form.get('release_date', None)

            if new_title is not None:
                movies.title = new_title
            else:
                movies.movies = old_title
    
            if new_release_date is not None:
                movies.release_date = new_release_date
            else:
                movies.release_date = old_release_date

            movies.update()

            return jsonify({
                'success': True
            }), 200
        except BaseException:
            abort(422)


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
                'success': True
            }), 200

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
                'success': True
            }), 200

    except BaseException:
        abort(422)


# Error Handling

@app.errorhandler(400)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
