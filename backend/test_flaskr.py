import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class FriviaTestCase(unittest.TestCase):
    """This class represents the frivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "frivia_test"
        self.database_path = "postgresql:///{}".format(self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is the capital of Hawaii',
            'answer': 'Honolulu',
            'category': 3,
            'difficulty': 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    def test_404_requesting_beyond_valid_page(self):
        pass
    def test_get_question_search_with_results(self):
        pass
    def test_get_question_search_without_results(self):
        pass
    def test_get_categories(self):
        pass
    def test_get_categories_method_not_allowed(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)

    def test_get_questions_by_category(self):
        pass
    def test_404_get_questions_by_category(self):
        pass
    def test_create_question(self):
        pass
    def test_422_if_book_creation_fails(self):
        pass
    def test_delete_question(self):
        pass
    def test_422_delete_if_question_not_exist(self):
        pass
    def test_get_quiz(self):
        pass
    def test_422_get_quiz(self):
        pass
    def test_404_get_quiz_no_category(self):
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
