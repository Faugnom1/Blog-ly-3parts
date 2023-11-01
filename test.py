import unittest
from app import app, db
from models import User, Post, Tag

class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_db'  # Use a testing database
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_root_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_show_users_route(self):
        response = self.client.get('/users/all_users')
        self.assertEqual(response.status_code, 200)

    def test_show_user_route(self):
        # Create a user for testing
        user = User(first_name="Test", last_name="User")
        with app.app_context():
            db.session.add(user)
            db.session.commit()

        response = self.client.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)

    def test_tags_index_route(self):
        response = self.client.get('/tags')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()