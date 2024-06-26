from flask import Flask, make_response, jsonify, request, session
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_cors import CORS
from flask_mail import Mail, Message
from models import User, SalesCall, Rating, Stage, Opportunity, Customer, db
from werkzeug.security import check_password_hash
import os
from config import *
from datetime import datetime

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
app.secret_key = os.environ.get('SECRET_KEY', 'mysecretkey')
app.json.compact = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)
api = Api(app)
mail = Mail(app)

@app.route("/")
def index():
    return "<h1>Sales Tracker</h1>"

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        session['user_id'] = user.id
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
    return make_response(jsonify({"error": "Unauthorized"}), 401)

@app.route("/logout", methods=["POST"])
def logout():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out"}), 200

class SalesCalls(Resource):
    def post(self):
        data = request.get_json()
        required_fields = ['user_id', 'customer_id', 'date', 'rating_id', 'stage_id']
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]

        print(f"Received data: {data}")  # Log the incoming data
        if missing_fields:
            print(f"Missing fields: {missing_fields}")  # Log any missing fields
            return make_response(jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400)

        try:
            new_call = SalesCall(
                user_id=data['user_id'],
                customer_id=data['customer_id'],
                date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
                notes=data.get('notes', ''),
                rating_id=data['rating_id'],
                stage_id=data['stage_id']
            )
            db.session.add(new_call)
            db.session.commit()
        except Exception as e:
            print(f"Error: {str(e)}") 
            return make_response(jsonify({"error": str(e)}), 400)

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
            password_hash=generate_password_hash(data['password'])
        )
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify(new_user.to_dict_custom()), 201)

api.add_resource(Users, '/users')

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

api.add_resource(UserById, '/users/<int:id>')

class UserCustomers(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)
        customers = [customer.to_dict_custom() for customer in user.customers]
        return make_response(jsonify(customers), 200)

api.add_resource(UserCustomers, '/users/<int:user_id>/customers')

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

api.add_resource(Ratings, '/ratings')

class RatingById(Resource):
    def get(self, id):
        rating = Rating.query.get(id)
        if not rating:
            return make_response({"error": "Rating not found"}, 404)
        return make_response(jsonify(rating.to_dict_custom()), 200)

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

api.add_resource(Stages, '/stages')

class StageById(Resource):
    def get(self, id):
        stage = Stage.query.get(id)
        if not stage:
            return make_response({"error": "Stage not found"}, 404)
        return make_response(jsonify(stage.to_dict_custom()), 200)

api.add_resource(StageById, '/stages/<int:id>')

class Opportunities(Resource):
    def get(self):
        opportunities = [opportunity.to_dict_custom() for opportunity in Opportunity.query.all()]
        return make_response(jsonify(opportunities), 200)
    
    def post(self):
        data = request.get_json()
        required_fields = ['description', 'customer_id', 'sales_call_id']
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]

        print(f"Received data: {data}")  # Log the incoming data
        if missing_fields:
            print(f"Missing fields: {missing_fields}")  # Log any missing fields
            return make_response(jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400)

        try:
            new_opportunity = Opportunity(
                description=data['description'],
                sales_call_id=int(data['sales_call_id']),
                customer_id=int(data['customer_id'])
            )
            db.session.add(new_opportunity)
            db.session.commit()
        except Exception as e:
            print(f"Error: {str(e)}")  # Log any exceptions
            return make_response(jsonify({"error": str(e)}), 400)

        return make_response(jsonify(new_opportunity.to_dict_custom()), 201)

api.add_resource(Opportunities, '/opportunities')

class OpportunityById(Resource):
    def get(self, id):
        opportunity = Opportunity.query.get(id)
        if not opportunity:
            return make_response({"error": "Opportunity not found"}, 404)
        return make_response(jsonify(opportunity.to_dict_custom()), 200)

    def patch(self, id):
        opportunity = Opportunity.query.get(id)
        if not opportunity:
            return make_response({"error": "Opportunity not found"}, 404)
        for attr in request.get_json():
            setattr(opportunity, attr, request.get_json()[attr])
        db.session.commit()
        return make_response(jsonify(opportunity.to_dict_custom()), 200)

    def delete(self, id):
        opportunity = Opportunity.query.get(id)
        if not opportunity:
            return make_response({"error": "Opportunity not found"}, 404)
        db.session.delete(opportunity)
        db.session.commit()
        return '', 204

api.add_resource(OpportunityById, '/opportunities/<int:id>')

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

api.add_resource(UserOpportunities, '/users/<int:user_id>/opportunities')

class Customers(Resource):
    def get(self):
        customers = [customer.to_dict_custom() for customer in Customer.query.all()]
        return make_response(jsonify(customers), 200)
    
    def post(self):
        data = request.get_json()
        required_fields = ['name', 'email', 'user_id']
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]

        if missing_fields:
            return make_response(jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400)

        new_customer = Customer(
            name=data['name'],
            email=data['email'],
            user_id=data['user_id']
        )
        db.session.add(new_customer)
        db.session.commit()
        return make_response(jsonify(new_customer.to_dict_custom()), 201)

api.add_resource(Customers, '/customers')

class CustomerById(Resource):
    def get(self, id):
        customer = Customer.query.get(id)
        if not customer:
            return make_response({"error": "Customer not found"}, 404)
        return make_response(jsonify(customer.to_dict_custom()), 200)

    def patch(self, id):
        customer = Customer.query.get(id)
        if not customer:
            return make_response({"error": "Customer not found"}, 404)
        for attr in request.get_json():
            setattr(customer, attr, request.get_json()[attr])
        db.session.commit()
        return make_response(jsonify(customer.to_dict_custom()), 200)

    def delete(self, id):
        customer = Customer.query.get(id)
        if not customer:
            return make_response({"error": "Customer not found"}, 404)
        db.session.delete(customer)
        db.session.commit()
        return '', 204

api.add_resource(CustomerById, '/customers/<int:id>')

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