import os
from flask import Flask, make_response, jsonify, request
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail, Message
from models import User, SalesCall, Rating, Stage, Opportunity, db

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'false').lower() in ['true', 'on', '1']
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app)
api = Api(app)
mail = Mail(app)

@app.route("/")
def index():
    return "<h1>Sales Tracker</h1>"

class SalesCalls(Resource):
    def get(self):
        sales_calls = [call.to_dict_custom() for call in SalesCall.query.all()]
        return make_response(jsonify(sales_calls), 200)
   
    def post(self):
        data = request.get_json()
        new_call = SalesCall(
            user_id=data['user_id'],
            date=data['date'],
            notes=data['notes'],
            rating_id=data['rating_id'],
            stage_id=data['stage_id']
        )
        db.session.add(new_call)
        db.session.commit()
        return make_response(jsonify(new_call.to_dict_custom()), 201)

api.add_resource(SalesCalls, '/sales_calls')

class SalesCallById(Resource):
    def get(self, id):
        call = SalesCall.query.get(id)
        if call is None:
            return make_response(jsonify(error='Sales Call not found'), 404)
        return make_response(jsonify(call.to_dict_custom()), 200)
    
    def patch(self, id):
        call = SalesCall.query.get(id)
        if call is None:
            return make_response(jsonify(error='Sales Call not found'), 404)
        for attr in request.get_json():
            setattr(call, attr, request.get_json()[attr])
        db.session.commit()
        return make_response(jsonify(call.to_dict_custom()), 200)
    
    def delete(self, id):
        call = SalesCall.query.get(id)
        if call is None:
            return make_response(jsonify(error='Sales Call not found'), 404)
        db.session.delete(call)
        db.session.commit()
        return make_response('', 204)

api.add_resource(SalesCallById, '/sales_calls/<int:id>')

class Users(Resource):
    def get(self):
        users = [user.to_dict_custom() for user in User.query.all()]
        return make_response(jsonify(users), 200)
    
    def post(self):
        data = request.get_json()
        new_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash']
        )
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify(new_user.to_dict_custom()), 201)

class UserById(Resource):
    def get(self, id):
        user = User.query.get(id)
        if not user:
            return make_response({"error": "User not found"}, 404)
        return make_response(jsonify(user.to_dict_custom()), 200)

    def patch(self, id):
        user = User.query.get(id)
        if not user:
            return make_response({"error": "User not found"}, 404)
        for attr in request.get_json():
            setattr(user, attr, request.get_json()[attr])
        db.session.commit()
        return make_response(jsonify(user.to_dict_custom()), 200)

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            return make_response({"error": "User not found"}, 404)
        db.session.delete(user)
        db.session.commit()
        return make_response('', 204)

api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<int:id>')

class Ratings(Resource):
    def get(self):
        ratings = [rating.to_dict_custom() for rating in Rating.query.all()]
        return make_response(jsonify(ratings), 200)
    
    def post(self):
        data = request.get_json()
        new_rating = Rating(
            value=data['value']
        )
        db.session.add(new_rating)
        db.session.commit()
        return make_response(jsonify(new_rating.to_dict_custom()), 201)

class RatingById(Resource):
    def get(self, id):
        rating = Rating.query.get(id)
        if not rating:
            return make_response({"error": "Rating not found"}, 404)
        return make_response(jsonify(rating.to_dict_custom()), 200)

api.add_resource(Ratings, '/ratings')
api.add_resource(RatingById, '/ratings/<int:id>')

class Stages(Resource):
    def get(self):
        stages = [stage.to_dict_custom() for stage in Stage.query.all()]
        return make_response(jsonify(stages), 200)
    
    def post(self):
        data = request.get_json()
        new_stage = Stage(
            name=data['name']
        )
        db.session.add(new_stage)
        db.session.commit()
        return make_response(jsonify(new_stage.to_dict_custom()), 201)

class StageById(Resource):
    def get(self, id):
        stage = Stage.query.get(id)
        if not stage:
            return make_response({"error": "Stage not found"}, 404)
        return make_response(jsonify(stage.to_dict_custom()), 200)

api.add_resource(Stages, '/stages')
api.add_resource(StageById, '/stages/<int:id>')

class Opportunities(Resource):
    def get(self):
        opportunities = [opportunity.to_dict_custom() for opportunity in Opportunity.query.all()]
        return make_response(jsonify(opportunities), 200)
    
    def post(self):
        data = request.get_json()
        new_opportunity = Opportunity(
            description=data['description'],
            sales_call_id=data['sales_call_id']
        )
        db.session.add(new_opportunity)
        db.session.commit()
        return make_response(jsonify(new_opportunity.to_dict_custom()), 201)

class OpportunityById(Resource):
    def get(self, id):
        opportunity = Opportunity.query.get(id)
        if not opportunity:
            return make_response({"error": "Opportunity not found"}, 404)
        return make_response(jsonify(opportunity.to_dict_custom()), 200)

class UserOpportunities(Resource):
    def post(self, user_id):
        data = request.get_json()
        opportunity = Opportunity.query.get(data['opportunity_id'])
        user = User.query.get(user_id)
        if not opportunity or not user:
            return make_response({"error": "User or Opportunity not found"}, 404)
        user.opportunities.append(opportunity)
        db.session.commit()
        return make_response(jsonify(user.to_dict_custom()), 200)

api.add_resource(Opportunities, '/opportunities')
api.add_resource(OpportunityById, '/opportunities/<int:id>')
api.add_resource(UserOpportunities, '/users/<int:user_id>/opportunities')

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    if not data or 'email' not in data or 'subject' not in data or 'body' not in data:
        return make_response(jsonify({"error": "Invalid request"}), 400)
    
    msg = Message(
        subject=data['subject'],
        recipients=[data['email']],
        body=data['body']
    )
    mail.send(msg)
    return make_response(jsonify({"message": "Email sent"}), 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)