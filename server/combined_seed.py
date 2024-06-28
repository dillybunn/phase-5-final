from app import app
from config import db
from datetime import date
from models import User, SalesCall, Rating, Stage, Opportunity, Customer, user_opportunity
from werkzeug.security import generate_password_hash

if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")

        # Delete old data
        print("Deleting data...")
        db.session.execute(user_opportunity.delete())
        Opportunity.query.delete()
        SalesCall.query.delete()
        Rating.query.delete()
        Stage.query.delete()
        Customer.query.delete()
        User.query.delete()

        db.session.commit()

        # Create Users
        print("Creating users...")
        users = [
            User(username="JerryGarcia", email="jerry@example.com", password_hash=generate_password_hash("password1")),
            User(username="BobWeir", email="bob@example.com", password_hash=generate_password_hash("password2")),
            User(username="Pigpen", email="pigpen@example.com", password_hash=generate_password_hash("password3"))
        ]
        db.session.add_all(users)
        db.session.commit()

        # Create Ratings
        print("Creating ratings...")
        ratings = [
            Rating(value="Excellent"),
            Rating(value="Good"),
            Rating(value="Average"),
            Rating(value="Poor")
        ]
        db.session.add_all(ratings)
        db.session.commit()

        # Create Stages
        print("Creating stages...")
        stages = [
            Stage(name="Initial Contact"),
            Stage(name="Negotiation"),
            Stage(name="Proposal Sent"),
            Stage(name="Closed Deal")
        ]
        db.session.add_all(stages)
        db.session.commit()

        # Create Customers
        print("Creating customers...")
        customers = [
            Customer(name="Customer A", email="customerA@example.com", user_id=users[0].id, rating_id=ratings[0].id, stage_id=stages[0].id),
            Customer(name="Customer B", email="customerB@example.com", user_id=users[0].id, rating_id=ratings[1].id, stage_id=stages[1].id),
            Customer(name="Customer C", email="customerC@example.com", user_id=users[0].id, rating_id=ratings[2].id, stage_id=stages[2].id),
            Customer(name="Customer D", email="customerD@example.com", user_id=users[1].id, rating_id=ratings[3].id, stage_id=stages[3].id),
            Customer(name="Customer E", email="customerE@example.com", user_id=users[1].id, rating_id=ratings[0].id, stage_id=stages[0].id),
            Customer(name="Customer F", email="customerF@example.com", user_id=users[1].id, rating_id=ratings[1].id, stage_id=stages[1].id),
            Customer(name="Customer G", email="customerG@example.com", user_id=users[2].id, rating_id=ratings[2].id, stage_id=stages[2].id),
            Customer(name="Customer H", email="customerH@example.com", user_id=users[2].id, rating_id=ratings[3].id, stage_id=stages[3].id),
            Customer(name="Customer I", email="customerI@example.com", user_id=users[2].id, rating_id=ratings[0].id, stage_id=stages[0].id)
        ]
        db.session.add_all(customers)
        db.session.commit()

        # Create Sales Calls
        print("Creating sales calls...")
        sales_calls = [
            SalesCall(date=date(2024, 1, 1), notes="Great initial call", user_id=users[0].id, customer_id=customers[0].id, rating_id=ratings[0].id, stage_id=stages[0].id),
            SalesCall(date=date(2024, 1, 2), notes="Follow-up call", user_id=users[0].id, customer_id=customers[1].id, rating_id=ratings[1].id, stage_id=stages[1].id),
            SalesCall(date=date(2024, 1, 3), notes="Negotiation phase", user_id=users[0].id, customer_id=customers[2].id, rating_id=ratings[2].id, stage_id=stages[2].id),
            SalesCall(date=date(2024, 1, 4), notes="Closed the deal", user_id=users[1].id, customer_id=customers[3].id, rating_id=ratings[3].id, stage_id=stages[3].id),
            SalesCall(date=date(2024, 1, 5), notes="Initial contact", user_id=users[1].id, customer_id=customers[4].id, rating_id=ratings[0].id, stage_id=stages[0].id),
            SalesCall(date=date(2024, 1, 6), notes="Negotiation", user_id=users[1].id, customer_id=customers[5].id, rating_id=ratings[1].id, stage_id=stages[1].id),
            SalesCall(date=date(2024, 1, 7), notes="Follow-up", user_id=users[2].id, customer_id=customers[6].id, rating_id=ratings[2].id, stage_id=stages[2].id),
            SalesCall(date=date(2024, 1, 8), notes="Proposal sent", user_id=users[2].id, customer_id=customers[7].id, rating_id=ratings[3].id, stage_id=stages[3].id),
            SalesCall(date=date(2024, 1, 9), notes="Deal closed", user_id=users[2].id, customer_id=customers[8].id, rating_id=ratings[0].id, stage_id=stages[0].id)
        ]
        db.session.add_all(sales_calls)
        db.session.commit()

        # Create Opportunities
        print("Creating opportunities...")
        opportunities = [
            Opportunity(description="Follow up with ACME Corp.", sales_call_id=sales_calls[0].id, customer_id=customers[0].id),
            Opportunity(description="Demo with Globex Corporation", sales_call_id=sales_calls[1].id, customer_id=customers[1].id),
            Opportunity(description="Proposal for Initech", sales_call_id=sales_calls[2].id, customer_id=customers[2].id),
            Opportunity(description="Close deal with Umbrella Corp.", sales_call_id=sales_calls[3].id, customer_id=customers[3].id),
            Opportunity(description="Follow up with Stark Industries", sales_call_id=sales_calls[4].id, customer_id=customers[4].id),
            Opportunity(description="Demo with Wayne Enterprises", sales_call_id=sales_calls[5].id, customer_id=customers[5].id),
            Opportunity(description="Proposal for Oscorp", sales_call_id=sales_calls[6].id, customer_id=customers[6].id),
            Opportunity(description="Close deal with LexCorp", sales_call_id=sales_calls[7].id, customer_id=customers[7].id),
            Opportunity(description="Follow up with S.T.A.R. Labs", sales_call_id=sales_calls[8].id, customer_id=customers[8].id)
        ]
        db.session.add_all(opportunities)
        db.session.commit()

        print("Seeding done!")