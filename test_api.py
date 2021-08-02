import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies
import sys, json

from dotenv import load_dotenv
load_dotenv()

class TriviaTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = os.getenv('DATABASE_PAT')

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
#            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories_results(self):
        res = self.client().get('/actors')
        data = json.load(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

if __name__ == "__main__":
    unittest.main()