import unittest
from app import app, db
from models import Plant

class TestPlant(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use a separate test database
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()  # Clean up after tests

    def test_plant_by_id_patch_route_updates_is_in_stock(self):
        with app.app_context():
            plant = Plant(
                name="Test Plant",
                image="test.jpg",
                price=10.0,
                is_in_stock=True
            )
            db.session.add(plant)
            db.session.commit()

            response = self.app.patch('/plants/1', json={'is_in_stock': False})
            self.assertEqual(response.status_code, 200)
            # Add more assertions as needed

    # Other test methods...