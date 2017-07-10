from app import db
from app import validation_schema
from flask_bcrypt import Bcrypt
from marshmallow import ValidationError, fields, validates
import re
import os
import jwt
import datetime


class User(db.Model):
    """This class represents all users in the system"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    bucketlist = db.relationship('Bucketlist', backref='users')

    def __init__(self, username=None, email=None, password=None):
        """Initialize the parameters belonging to the user"""
        self.username = username
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def create_access_token(uid):
        try:
            payload = {
                    "exp": datetime.datetime.utcnow() +
                    datetime.timedelta(days=0, seconds=3600),
                    "iat": datetime.datetime.utcnow(),
                    "sub": uid}
            return jwt.encode(payload, os.getenv('SECRET'), algorithm='HS256')
        except Exception as e:
            return str(e)

    def decode_access_token(token):
        try:
            payload = jwt.decode(token, os.getenv('SECRET'))
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired"
        except jwt.InvalidTokenError:
            return "Invalid token"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Bucketlist(db.Model):
    """This class represents the Bucketlist table"""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('Item', backref='bucketlists',
                            cascade='all, delete-orphan', lazy='dynamic')
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """Initialize with name"""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)


class Item(db.Model):
    """This class represents the items table that are within the bucketlists"""

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    bucketlist_owner = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)

    def __init__(self, name, bucketlist_owner):
        """Initialize with name"""
        self.name = name
        self.bucketlist_owner = bucketlist_owner

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Item: {}>".format(self.name)


class UserSchema(validation_schema.ModelSchema):
    class Meta:
        model = User
    email = fields.Email(required=True)

    @validates('username')
    def validate_username(self, username):
        if username == "":
            raise ValidationError("User must have a username")
        elif not re.match("^[A-Za-z0-9]+$", username):
            raise ValidationError("Invalid username.")

    @validates("password")
    def validate_password(self, password):
        if password == "":
            raise ValidationError("User must have a password")
        elif not re.match("^[A-Za-z0-9]+$", password):
            raise ValidationError("""Invalid password. Does not accept special
            characters""")


class BucketlistSchema(validation_schema.ModelSchema):
    class Meta:
        model = Bucketlist

    @validates('name')
    def validate_name(self, name):
        if name == "":
            raise ValidationError("Bucketlist must have a name")
        elif not re.match("^[A-Za-z0-9]+\s?[A-Za-z0-9]+\s?[A-Za-z0-9]+\s?[A-Za-z0-9]+\s?[A-Za-z0-9]+$", name):
            raise ValidationError("Invalid name.")


class ItemSchema(validation_schema.ModelSchema):
    class Meta:
        model = Item

    @validates('name')
    def validate_name(self, name):
        if name == "":
            raise ValidationError("Item must have a name")
        elif not re.match("^[A-Za-z0-9]+\s?[A-Za-z0-9]+\s?[A-Za-z0-9]+\s?[A-Za-z0-9]+\s?[A-Za-z0-9]+$", name):
            raise ValidationError("Invalid name.")
