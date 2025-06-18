from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_migrate import Migrate
from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)


class CamperList(Resource):
    def get(self):
        campers = Camper.query.all()
        return [c.to_dict(only=('id', 'name', 'age')) for c in campers], 200

    def post(self):
        data = request.get_json()
        try:
            camper = Camper(name=data['name'], age=data['age'])
            db.session.add(camper)
            db.session.commit()
            return camper.to_dict(only=('id', 'name', 'age')), 201
        except ValueError:
            return {"errors": ["validation errors"]}, 400
        except Exception:
            return {"errors": ["validation errors"]}, 400


class CamperById(Resource):
    def get(self, id):
        camper = Camper.query.get(id)
        if camper:
            return camper.to_dict(
                only=('id', 'name', 'age'),
                include={'signups': {
                    'only': ('id', 'time', 'camper_id', 'activity_id'),
                    'include': {'activity': {'only': ('id', 'name', 'difficulty')}}
                }}
            ), 200
        return {'error': 'Camper not found'}, 404

    def patch(self, id):
        camper = Camper.query.get(id)
        if not camper:
            return {'error': 'Camper not found'}, 404

        data = request.get_json()
        try:
            if 'name' in data:
                camper.name = data['name']
            if 'age' in data:
                camper.age = data['age']
            db.session.commit()
            return camper.to_dict(only=('id', 'name', 'age')), 202
        except ValueError:
            return {"errors": ["validation errors"]}, 400
        except Exception:
            return {"errors": ["validation errors"]}, 400


class ActivityList(Resource):
    def get(self):
        activities = Activity.query.all()
        return [a.to_dict(only=('id', 'name', 'difficulty')) for a in activities], 200


class ActivityById(Resource):
    def delete(self, id):
        activity = Activity.query.get(id)
        if not activity:
            return {'error': 'Activity not found'}, 404

        db.session.delete(activity)
        db.session.commit()
        return {}, 204


class SignupList(Resource):
    def post(self):
        data = request.get_json()
        try:
            signup = Signup(
                camper_id=data['camper_id'],
                activity_id=data['activity_id'],
                time=data['time']
            )
            db.session.add(signup)
            db.session.commit()
            return signup.to_dict(
                only=('id', 'camper_id', 'activity_id', 'time'),
                include={
                    'camper': {'only': ('id', 'name', 'age')},
                    'activity': {'only': ('id', 'name', 'difficulty')}
                }
            ), 201
        except ValueError:
            return {"errors": ["validation errors"]}, 400
        except Exception:
            return {"errors": ["validation errors"]}, 400


api.add_resource(CamperList, '/campers')
api.add_resource(CamperById, '/campers/<int:id>')
api.add_resource(ActivityList, '/activities')
api.add_resource(ActivityById, '/activities/<int:id>')
api.add_resource(SignupList, '/signups')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
