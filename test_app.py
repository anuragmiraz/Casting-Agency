import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actors, Movies

from dotenv import load_dotenv
load_dotenv()

class FinalTestCase(unittest.TestCase):
    """This class represents the Final project test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        db_name = "final_test"
        db_host = os.getenv("DATABASE_HOST")  
        db_user = os.getenv("DATABASE_USER")
        db_password = os.getenv("DATABASE_PASSWORD")

        self.database_path = "postgres://{}:{}@{}/{}".format(db_user, db_password, db_host, db_name)

#        self.database_name = "trivia_test"
#        self.database_path = 'postgresql://postgres:doublea@localhost:5432/trivia_test'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

# My change starts
        self.new_actors = {
            'name': 'Anurag Agarwal',
            'age': 35,
            'gender': 'M'
        }

        self.wrong_actors = {
            'name': 'Anurag Agarwal',
            'age': 35
        }

        self.new_movies = {
            'title': 'Test movie',
            'release_date': '2021-02-02'
        }

        self.upd_movies = {
            'title': 'updated movie'
        }

        self.upd_actors = {
            'name': 'Ayaansh Agarwal'
        }

        self.new_movies = {
            'title': 'Test movie'
        }

# My change ends

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation
    and for expected errors.
    """


# GET ALL ACTORS

    def test_get_actors_results(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['actors'])
        self.assertEqual(data['success'], True)

    def test_get_actors_no_results(self):
        res = self.client().get('/actors/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

# GET ALL MOVIES

    def test_get_movies_results(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['movies'])
        self.assertEqual(data['success'], True)

    def test_get_movies_no_results(self):
        res = self.client().get('/movies/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

# DELETE AN ACTOR

    def test_delete_actors(self):
        res = self.client().delete('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/122221')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# DELETE A MOVIE

    def test_delete_movies(self):
        res = self.client().delete('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/122221')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

# CREATE / POST AN ACTOR

    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actors)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_actors_not_allowed(self):
        res = self.client().post('/actors', json=self.wrong_actors)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
    
# CREATE / POST A MOVIE

    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movies)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_movies_not_allowed(self):
        res = self.client().post('/movies', json=self.wrong_movies)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
    
# PATCH AN ACTOR

    def test_update_actor(self):
        res = self.client().patch('/actors/1', json=self.upd_actors)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_actors_not_allowed(self):
        res = self.client().patch('/actors/12222')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
# PATCH A MOVIE

    def test_update_movie(self):
        res = self.client().patch('/movies/1', json=self.upd_movies)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_movies_not_allowed(self):
        res = self.client().patch('/movies/12222')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
