from app import app
from config import db
from datetime import date
from models import User, SalesCall, Rating, Stage, Opportunity, Customer, user_opportunity, customer_opportunity

if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")

        # Delete old data
        print("Deleting data...")
        db.session.execute(user_opportunity.delete())
        db.session.execute(customer_opportunity.delete())
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
            User(username="jerrygarcia", email="jerry@example.com", password_hash="hashedpassword1"),
            User(username="bobweir", email="bob@example.com", password_hash="hashedpassword2"),
            User(username="pigpen", email="pigpen@example.com", password_hash="hashedpassword3")
        ]
        db.session.add_all(users)
        db.session.commit()

        # Create Customers
        print("Creating customers...")
        customers = [
            Customer(name="Customer A", email="customerA@example.com", phone="123-456-7890", address="123 Main St"),
            Customer(name="Customer B", email="customerB@example.com", phone="234-567-8901", address="456 Elm St"),
            Customer(name="Customer C", email="customerC@example.com", phone="345-678-9012", address="789 Oak St")
        ]
        db.session.add_all(customers)
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

        # Create Sales Calls
        print("Creating sales calls...")
        sales_calls = [
            SalesCall(date=date(2024, 1, 1), notes="Great initial call", user_id=users[0].id, rating_id=ratings[0].id, stage_id=stages[0].id, customer_id=customers[0].id),
            SalesCall(date=date(2024, 1, 2), notes="Follow-up call", user_id=users[1].id, rating_id=ratings[1].id, stage_id=stages[1].id, customer_id=customers[1].id),
            SalesCall(date=date(2024, 1, 3), notes="Negotiation phase", user_id=users[2].id, rating_id=ratings[2].id, stage_id=stages[2].id, customer_id=customers[2].id),
            SalesCall(date=date(2024, 1, 4), notes="Closed the deal", user_id=users[0].id, rating_id=ratings[3].id, stage_id=stages[3].id, customer_id=customers[0].id)
        ]
        db.session.add_all(sales_calls)
        db.session.commit()

        # Create Opportunities
        print("Creating opportunities...")
        opportunities = [
            Opportunity(description="Follow up with ACME Corp.", sales_call_id=sales_calls[0].id, customer_id=customers[0].id),
            Opportunity(description="Demo with Globex Corporation", sales_call_id=sales_calls[1].id, customer_id=customers[1].id),
            Opportunity(description="Proposal for Initech", sales_call_id=sales_calls[2].id, customer_id=customers[2].id),
            Opportunity(description="Close deal with Umbrella Corp.", sales_call_id=sales_calls[3].id, customer_id=customers[0].id)
        ]
        db.session.add_all(opportunities)
        db.session.commit()

        # Establish many-to-many relationships between users and opportunities
        print("Establishing user-opportunity relationships...")
        users[0].opportunities = [opportunities[0], opportunities[1]]
        users[1].opportunities = [opportunities[2]]
        users[2].opportunities = [opportunities[3]]
        db.session.commit()

        # Establish many-to-many relationships between customers and opportunities
        print("Establishing customer-opportunity relationships...")
        customers[0].opportunities = [opportunities[0], opportunities[3]]
        customers[1].opportunities = [opportunities[1]]
        customers[2].opportunities = [opportunities[2]]
        db.session.commit()

        print("Seeding done!")