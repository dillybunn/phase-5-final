from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from config import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Association table for the many-to-many relationship between User and Opportunity
user_opportunity = db.Table('user_opportunity',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('opportunity_id', db.Integer, db.ForeignKey('opportunities.id'), primary_key=True)
)

class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    sales_calls = db.relationship("SalesCall", back_populates="user", cascade="all, delete-orphan")
    opportunities = db.relationship("Opportunity", secondary=user_opportunity, back_populates="users")
    customers = db.relationship("Customer", back_populates="user", cascade="all, delete-orphan")

    serialize_rules = ('-sales_calls.user', '-opportunities.users', '-customers.user')

    def to_dict_custom(self, depth=1):
        if depth <= 0:
            return {'id': self.id, 'username': self.username, 'email': self.email}
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'sales_calls': [sc.to_dict_custom(depth - 1) for sc in self.sales_calls],
            'opportunities': [op.to_dict_custom(depth - 1) for op in self.opportunities],
            'customers': [cu.to_dict_custom(depth - 1) for cu in self.customers]
        }

    def __repr__(self):
        return f"<User: {self.username}>"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class SalesCall(db.Model, SerializerMixin):
    __tablename__ = "sales_calls"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    rating_id = db.Column(db.Integer, db.ForeignKey("ratings.id"), nullable=False)
    stage_id = db.Column(db.Integer, db.ForeignKey("stages.id"), nullable=False)

    user = db.relationship("User", back_populates="sales_calls")
    customer = db.relationship("Customer", back_populates="sales_calls")
    rating = db.relationship("Rating", back_populates="sales_calls")
    stage = db.relationship("Stage", back_populates="sales_calls")
    opportunities = db.relationship("Opportunity", back_populates="sales_call", cascade='all, delete-orphan')

    serialize_rules = ('-user.sales_calls', '-customer.sales_calls', '-rating.sales_calls', '-stage.sales_calls')

    @validates('date')
    def validate_date(self, key, date):
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d').date()
        return date

    def to_dict_custom(self, depth=1):
        if depth <= 0:
            return {'id': self.id, 'date': self.date, 'notes': self.notes}
        return {
            'id': self.id,
            'date': self.date,
            'notes': self.notes,
            'user': self.user.to_dict_custom(depth - 1) if self.user else None,
            'customer': self.customer.to_dict_custom(depth - 1) if self.customer else None,
            'rating': self.rating.to_dict_custom(depth - 1) if self.rating else None,
            'stage': self.stage.to_dict_custom(depth - 1) if self.stage else None,
            'opportunities': [op.to_dict_custom(depth - 1) for op in self.opportunities]
        }

    def __repr__(self):
        return f"<SalesCall: {self.date}, User: {self.user_id}, Customer: {self.customer_id}, Rating: {self.rating_id}, Stage: {self.stage_id}>"

class Rating(db.Model, SerializerMixin):
    __tablename__ = "ratings"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String, nullable=False)

    sales_calls = db.relationship("SalesCall", back_populates="rating")

    serialize_rules = ('-sales_calls.rating',)

    def to_dict_custom(self, depth=1):
        if depth <= 0:
            return {'id': self.id, 'value': self.value}
        return {
            'id': self.id,
            'value': self.value,
            'sales_calls': [sc.to_dict_custom(depth - 1) for sc in self.sales_calls]
        }

    def __repr__(self):
        return f"<Rating: {self.value}>"

class Stage(db.Model, SerializerMixin):
    __tablename__ = "stages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    sales_calls = db.relationship("SalesCall", back_populates="stage")

    serialize_rules = ('-sales_calls.stage',)

    def to_dict_custom(self, depth=1):
        if depth <= 0:
            return {'id': self.id, 'name': self.name}
        return {
            'id': self.id,
            'name': self.name,
            'sales_calls': [sc.to_dict_custom(depth - 1) for sc in self.sales_calls]
        }

    def __repr__(self):
        return f"<Stage: {self.name}>"

class Opportunity(db.Model, SerializerMixin):
    __tablename__ = "opportunities"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    sales_call_id = db.Column(db.Integer, db.ForeignKey("sales_calls.id"), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)

    sales_call = db.relationship("SalesCall", back_populates="opportunities")
    customer = db.relationship("Customer", back_populates="opportunities")
    users = db.relationship("User", secondary=user_opportunity, back_populates="opportunities")

    serialize_rules = ('-sales_call.opportunities', '-customer.opportunities', '-users.opportunities')

    def to_dict_custom(self, depth=1):
        if depth <= 0:
            return {'id': self.id, 'description': self.description}
        return {
            'id': self.id,
            'description': self.description,
            'sales_call': self.sales_call.to_dict_custom(depth - 1) if self.sales_call else None,
            'customer': self.customer.to_dict_custom(depth - 1) if self.customer else None,
            'users': [user.to_dict_custom(depth - 1) for user in self.users]
        }

    def __repr__(self):
        return f"<Opportunity: {self.description}>"

class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    rating_id = db.Column(db.Integer, db.ForeignKey("ratings.id"))
    stage_id = db.Column(db.Integer, db.ForeignKey("stages.id"))

    user = db.relationship("User", back_populates="customers")
    sales_calls = db.relationship("SalesCall", back_populates="customer", cascade='all, delete-orphan')
    opportunities = db.relationship("Opportunity", back_populates="customer", cascade='all, delete-orphan')
    rating = db.relationship("Rating")
    stage = db.relationship("Stage")

    serialize_rules = ('-user.customers', '-sales_calls.customer', '-opportunities.customer')

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address, "Provided email address is not valid."
        return address

    def to_dict_custom(self, depth=1):
        if depth <= 0:
            return {'id': self.id, 'name': self.name, 'email': self.email}
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'user': self.user.to_dict_custom(depth - 1) if self.user else None,
            'sales_calls': [sc.to_dict_custom(depth - 1) for sc in self.sales_calls],
            'opportunities': [op.to_dict_custom(depth - 1) for op in self.opportunities],
            'rating': self.rating.to_dict_custom(depth - 1) if self.rating else None,
            'stage': self.stage.to_dict_custom(depth - 1) if self.stage else None,
        }

    def __repr__(self):
        return f"<Customer: {self.name}>"