from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)

class PlantByID(Resource):
    def get(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return {"error": "Plant not found"}, 404
        return plant.to_dict(), 200

    def patch(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return {"error": "Plant not found"}, 404

        data = request.get_json()
        if 'is_in_stock' in data:
            plant.is_in_stock = data['is_in_stock']
            db.session.commit()
            return plant.to_dict(), 200

        return {"error": "Invalid data"}, 400

    def delete(self, id):
        plant = db.session.get(Plant, id)
        if not plant:
            return {"error": "Plant not found"}, 404

        db.session.delete(plant)
        db.session.commit()
        return '', 204

api.add_resource(PlantByID, '/plants/<int:id>')

with app.app_context():
    db.create_all()
