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

        prod_token = os.getenv("PRODUCER")
        dirc_token = os.getenv("DIRECTOR")
        asst_token = os.getenv("ASSISTANT")

        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = os.getenv('DATABASE_PAT')
        
        self.producer = {'Authorization': 
                        'Bearer ' + prod_token}
        self.assistant = {'Authorization': 
                        'Bearer ' + asst_token}
        self.director = {'Authorization': 
                        'Bearer ' + dirc_token}

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
#            self.db.create_all()

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
            'name': 'updated actor'
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
            print("success1")
        except:
            print("error1")
            print(sys.exc_info())

    def test_get_all_movies_results(self):
        try:
            res = self.client().get('/movies')
            data = json.loads(res.data)
        
            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['movies'])
            self.assertEqual(data['success'], True)
            print("success2")
        except:
            print("error2")
            print(sys.exc_info())

    def test_get_actors_det_results(self):
        try:
            res = self.client().get('/actors-details/3', 
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['actors'])
            self.assertEqual(data['success'], True)
            print("success3")
        except:
            print("error3")
            print(sys.exc_info())

    def test_get_actors_no_results(self):
        try:
            res = self.client().get('/actors-details/10000',
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            print("success4")
        except:
            print("error4")
            print(sys.exc_info())

    def test_get_movies_results(self):
        try:
            res = self.client().get('/movies-details/4',
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            print("success5")
        except:
            print("error5")
            print(sys.exc_info())

    def test_get_movies_no_results(self):
        try:
            res = self.client().get('/movies-details/10000',
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            print("success6")
        except:
            print("error6")
            print(sys.exc_info())

    def test_create_new_actor(self):
        try:
            res = self.client().post('/actors', json=self.new_actors,
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            print("success7")
        except:
            print("error7")
            print(sys.exc_info())

    def test_create_new_actors_not_allowed(self):
        try:
            res = self.client().post('/actors', json=self.wrong_actors,
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            print("success8")
        except:
            print("error8")
            print(sys.exc_info())

    def test_create_new_movie(self):
        try:
            res = self.client().post('/movies', json=self.new_movies,
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            print("success9")
        except:
            print("error9")
            print(sys.exc_info())

    def test_create_new_movies_not_allowed(self):
        try:
            res = self.client().post('/movies', json=self.wrong_movies,
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 422)
            self.assertEqual(data['success'], False)
            print("success0")
        except:
            print("error0")
            print(sys.exc_info())

    def test_update_actor(self):
        try:
            res = self.client().patch('/actors/3', json=self.upd_actors,
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            print("successa")
        except:
            print("errora")
            print(sys.exc_info())

    def test_update_actors_not_allowed(self):
        try:
            res = self.client().patch('/actors/12222', json=self.upd_actors,
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            print("successb")
        except:
            print("errorb")
            print(sys.exc_info())

    def test_update_movie(self):
        try:
            res = self.client().patch('/movies/4', json=self.upd_movies,
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            print("successc")
        except:
            print("errorc")
            print(sys.exc_info())

    def test_create_prod_movies_not_allowed(self):
        try:
            res = self.client().patch('/movies/12222', json=self.upd_movies,
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            print("successd")
        except:
            print("errord")
            print(sys.exc_info())

    def test_delete_actors(self):
        try:
            res = self.client().delete('/actors/6',
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            print("successe")
        except:
            print("errore")
            print(sys.exc_info())

    def test_if_actor_does_not_exist(self):
        try:
            res = self.client().delete('/actors/122221',
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found')
            print("successf")
        except:
            print("errorf")
            print(sys.exc_info())

    def test_delete_movies(self):
        try:
            res = self.client().delete('/movies/4',
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            print("successg")
        except:
            print("errorg")
            print(sys.exc_info())

    def test_if_movie_does_not_exist(self):
        try:
            res = self.client().delete('/movies/122221',
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found')
            print("successh")
        except:
            print("errorh")
            print(sys.exc_info())

    def test_get_actors_results_asst(self):
        try:
            res = self.client().get('/actors-details/3', 
            headers=self.assistant)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['actors'])
            self.assertEqual(data['success'], True)
            print("successi")
        except:
            print("errori")
            print(sys.exc_info())

    def test_get_actors_results_dirc(self):
        try:
            res = self.client().get('/actors-details/3', 
            headers=self.director)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['actors'])
            self.assertEqual(data['success'], True)
            print("successj")
        except:
            print("errorj")
            print(sys.exc_info())

    def test_get_actors_results(self):
        try:
            res = self.client().get('/actors-details/3', 
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertTrue(data['actors'])
            self.assertEqual(data['success'], True)
            print("successk")
        except:
            print("errork")
            print(sys.exc_info())

    def test_create_new_actor_prod(self):
        try:
            res = self.client().post('/actors', json=self.new_actors,
            headers=self.producer)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            print("successl")
        except:
            print("errorl")
            print(sys.exc_info())

    def test_create_new_actor_dirc(self):
        try:
            res = self.client().post('/actors', json=self.new_actors,
            headers=self.director)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            print("successm")
        except:
            print("errorm")
            print(sys.exc_info())

    def test_create_new_actor_asst(self):
        try:
            res = self.client().post('/actors', json=self.new_actors,
            headers=self.assistant)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 403)
            self.assertEqual(data['success'], False)
            print("successn")
        except:
            print("errorn")
            print(sys.exc_info())

if __name__ == "__main__":
    unittest.main()