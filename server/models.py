from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from config import *

class Owner(db.Model, SerializerMixin):
    __tablename__ = "owners"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.Integer)
    address = db.Column(db.String)

    # add relationships test
    visits = db.relationship("Visit", back_populates="owner")
    pets = db.relationship("Pet", back_populates="owner")
    sitters = association_proxy("visits", "sitter")

    @hybrid_property
    def unique_sitters(self):
        sitter_list = [visit.sitter for visit in self.visits]
        unique_sitter_list = list(set(sitter_list))
        return unique_sitter_list
    # add serialization rules
    serialize_rules = ('-visits.owner', '-pets.owner', 'sitters')

    # add validation
    @validates("phone")
    def validate_phone(self, _, phone):
        if not isinstance(phone, int) or (len(str(phone)) != 10):
            raise ValueError("Phone must be an integer with 10 characters, no spaces")
        return phone

    def __repr__(self):
        return f"<Owner: {self.name}>"
    
class Pet(db.Model, SerializerMixin):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    animal = db.Column(db.String)
    breed = db.Column(db.String)
    age = db.Column(db.Integer)
    temperament = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=False)
    
    owner = db.relationship('Owner', back_populates='pets')
    visits = db.relationship('Visit', back_populates='pet')

    def __repr__(self):
        return f'<Pet {self.id}, {self.name}, {self.image}, {self.animal}, {self.breed}, {self.age}, {self.temperament}, Owner: {self.owner_id}>'

    serialize_rules = ('-owner.pets', '-visits.pet', '-owner.visits')
    
    
    # validates name to be less than 50 // breaking the edit code
    
    # @validates('name')
    # def validate_name(self, key, name):
    #     if not name:
    #         raise ValueError("Pet need a name")
    #     if len(name) > 50:
    #         raise ValueError("name too big")
        
        
    # validate age to be only numbers
    
    # @validates('age')
    # def validate_age(self, key, age):
    #     if not str(age).isnumeric():
    #         raise ValueError("Age must be a number")
    #     return age
    
    # validate to be only cat or dog. not sure if we want to add that ??
    
    # @validates('animal')
    # def validate_animal(self, key, animal):
    #     animal = animal.lower()
    #     if animal not in ["dog", "cat"]:
    #         raise ValueError("Animal must be either 'dog' or 'cat'")
    #     return animal

    #test
        
    
    
class Sitter(db.Model, SerializerMixin):
    __tablename__ = "sitters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)

    visits = db.relationship('Visit', back_populates='sitter', cascade='all, delete-orphan')
    owners = association_proxy('visits', 'owner')

    serialize_rules = ('-visits.sitter', '-owners.sitters', '-visits.owner', '-visits.pet')

    @validates("phone")
    def validate_phone(self, _, phone):
        if not isinstance(phone, int) or (len(str(phone)) != 10):
            raise ValueError("Phone must be an integer with 10 characters, no spaces")
        return phone
    
    @validates("experience")
    def validate_experience(self, _, experience):
        if not isinstance(experience, int) or (experience > 10):
            raise ValueError("Experience must be an integer between 1 and 10")
        return experience

def repr(self):
        return f"<Sitter: {self.name}, Experience: {self.experience} years>"

class Visit(db.Model, SerializerMixin):
    __tablename__ = "visits"

    id = db.Column(db.Integer, primary_key=True)
    visit_notes = db.Column(db.String)
    sitter_id = db.Column(db.Integer, db.ForeignKey("sitters.id"), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey("pets.id"), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("owners.id"), nullable=False)
    date = db.Column(db.Date)
    check_in_time = db.Column(db.Time)

    # add relationships
    owner = db.relationship("Owner", back_populates="visits")
    sitter = db.relationship("Sitter", back_populates="visits")
    pet = db.relationship("Pet", back_populates="visits")

    # add serialization rules
    serialize_rules = ('-owner.visits', '-sitter.visits', '-pet.visits', '-owner.pets', '-sitter.owners')

    def __repr__(self):
        return f"<Visit: {self.date}>"