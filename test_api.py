import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies
import sys, json

from dotenv import load_dotenv
load_dotenv()

class CastingTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = os.getenv('DATABASE_PAT')
        self.assistant = os.getenv("ASSISTANT")
        self.director = os.getenv("DIRECTOR")
        self.producer = os.getenv("PRODUCER")

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

        self.new_actors = {
            'name': 'Modi',
            'age': 75,
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

        self.wrong_movies = {
            'title': 'Test movie'
        }

        self.upd_movies = {
            'title': 'updated movie'
        }

        self.upd_actors = {
            'name': 'Narendra modi'
        }

    def tearDown(self):
        pass

    def test_get_all_actors_results(self):
        try:
            res = self.client().get('/actors')
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['actors'])
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_get_all_movies_results(self):
        try:
            res = self.client().get('/movies')
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['movies'])
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_get_actors_det_results(self):
        try:
            res = self.client().get('/actors-details/1', 
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['actors'])
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_get_actors_no_results(self):
        try:
            res = self.client().get('/actors-details/10000',
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
        except:
            print(sys.exc_info())

    def test_get_movies_results(self):
        try:
            res = self.client().get('/movies-details/1',
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_get_movies_no_results(self):
        try:
            res = self.client().get('/movies-details/10000',
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
        except:
            print(sys.exc_info())

    def test_create_new_actor(self):
        try:
            res = self.client().post('/actors', json=self.new_actors,
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_create_new_actors_not_allowed(self):
        try:
            res = self.client().post('/actors', json=self.wrong_actors,
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
        except:
            print(sys.exc_info())
    
    def test_create_new_movie(self):
        try:
            res = self.client().post('/movies', json=self.new_movies,
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_create_new_movies_not_allowed(self):
        try:
            res = self.client().post('/movies', json=self.wrong_movies,
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
        except:
            print(sys.exc_info())

    def test_update_actor(self):
        try:
            res = self.client().patch('/actors/1', json=self.upd_actors,
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_update_actors_not_allowed(self):
        try:
            res = self.client().patch('/actors/12222', json=self.upd_actors,
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
        except:
            print(sys.exc_info())
    
    def test_update_movie(self):
        try:
            res = self.client().patch('/movies/1', json=self.upd_movies,
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_create_prod_movies_not_allowed(self):
        try:
            res = self.client().patch('/movies/12222', json=self.upd_movies,
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
        except:
            print(sys.exc_info())

    def test_delete_actors(self):
        try:
            res = self.client().delete('/actors/1',
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_if_actor_does_not_exist(self):
        try:
            res = self.client().delete('/actors/122221',
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found')
        except:
            print(sys.exc_info())

    def test_delete_movies(self):
        try:
            res = self.client().delete('/movies/1',
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_if_movie_does_not_exist(self):
        try:
            res = self.client().delete('/movies/122221',
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found')
        except:
            print(sys.exc_info())

    def test_get_actors_results_asst(self):
        try:
            res = self.client().get('/actors-details/3', 
            headers={'Authorization': "Bearer {}".format(self.assistant)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['actors'])
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_get_actors_results_dirc(self):
        try:
            res = self.client().get('/actors-details/3', 
            headers={'Authorization': "Bearer {}".format(self.director)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['actors'])
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_get_actors_results(self):
        try:
            res = self.client().get('/actors-details/3', 
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['actors'])
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_create_new_actor_prod(self):
        try:
            res = self.client().post('/actors', json=self.new_actors,
            headers={'Authorization': "Bearer {}".format(self.producer)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_create_new_actor_dirc(self):
        try:
            res = self.client().post('/actors', json=self.new_actors,
            headers={'Authorization': "Bearer {}".format(self.director)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

    def test_create_new_actor_asst(self):
        try:
            res = self.client().post('/actors', json=self.new_actors,
            headers={'Authorization': "Beaer {}".format(self.assistant)})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 403)
            self.assertEqual(data['success'], True)
        except:
            print(sys.exc_info())

if __name__ == "__main__":
    unittest.main()