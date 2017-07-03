from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import request, jsonify, abort
from functools import wraps
from flask_bcrypt import Bcrypt
from instance.config import app_config


db = SQLAlchemy()
validation_schema = Marshmallow()

from app.models import User, UserSchema


def create_app(config_name):
    """This function creates the actual application to be used and consumed
    within the API"""
    from app.models import Bucketlist
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    validation_schema.init_app(app)

    @app.errorhandler(404)
    def unknown_page(e):
        response = jsonify({"error": "Resource not found"})
        response.status_code = 404
        return response

    @app.errorhandler(500)
    def internal_server_error(e):
        response = jsonify({"error": "The basis of the request is incorrect"})
        response.status_code = 500
        return response

    def check_token(func):
        @wraps(func)
        def required_token(*args, **kwargs):
            if request.headers.get("Authorization"):
                token = bytes(request.headers.get("Authorization").
                              split(" ")[1], "utf-8")
                user_id = User.decode_access_token(token)
                if user_id and isinstance(user_id, int):
                    return func(*args, **kwargs)
                else:
                    return jsonify({"msg": "Access denied."})
            else:
                return jsonify({"msg": "Access denied."})
        return required_token

    @app.route('/auth/register', methods=['POST'])
    def register():
        """This function registers the user who will create the bucketlists"""
        username = str(request.data.get('username', ''))
        email = str(request.data.get('email', ''))
        password = str(request.data.get('password', ''))
        if username:
            if User.query.filter_by(username=username).first():
                response = jsonify({'msg': "Username unavailable"})
                response.status_code = 200
                return response
            if email:
                if User.query.filter_by(email=email).first():
                    response = jsonify({'msg': "Email already in use"})
                    response.status_code = 200
                    return response
                if password:
                    print(username, email, password)
                    errors = UserSchema().validate({"username": username,
                                                    "email": email,
                                                    "password": password},
                                                   partial=True)
                    if errors:
                        return jsonify(errors)
                    user = User(username=username, email=email,
                                password=password)
                    user.save()
                    response = jsonify({'msg':
                                        "User has been created successfully"})
                    response.status_code = 201
                    return response
                else:
                    response = jsonify({'msg':
                                        "User must have a password"})
                    response.status_code = 200
                    return response
            else:
                response = jsonify({'msg':
                                    "User must have an email"})
                response.status_code = 200
                return response
        else:
            response = jsonify({'msg':
                                "User must have a username"})
            response.status_code = 200
            return response

    @app.route('/auth/login', methods=['POST'])
    def login():
        """This function handles the log in process of a registered
         user"""
        username = request.data.get('username', False)
        password = request.data.get('password', False)
        if username and password:
            errors = UserSchema().validate({"username": username,
                                           "password": password},
                                           partial=True)
            if errors:
                return errors

        user = User.query.filter_by(username=username).first()
        if user:
            if Bcrypt().check_password_hash(user.password, password):
                access_token = User.create_access_token(user.id)
                return jsonify({"token": access_token.decode()})
        else:
            response = jsonify({"msg": "Username and password invalid."})
            response.status_code = 401
        return username

    @app.route('/bucketlists', methods=['POST', 'GET'])
    @check_token
    def bucketlists():
        """This function does the actual creation of the bucketlist within the
        API"""
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                bucketlist = Bucketlist(name=name)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
                response.status_code = 201
                return response
        else:
            # GET
            bucketlists = Bucketlist.get_all()
            results = []

            for bucketlist in bucketlists:
                obj = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                results.append(obj)
            if len(results) < 1:
                results = {'msg': "There are no bucketlists in the system"}
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
    @check_token
    def bucketlist_management(id, **kwargs):
        """This function handles all the management functions of the bucketlist
        """
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            abort(404)

        if request.method == 'DELETE':
            bucketlist.delete()
            return {"message": "The bucketlist {} has been succesfully"
                    .format(bucketlist.id)}, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            bucketlist.name = name
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified})
            response.status_code = 200
            return response

        else:  # GET
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified})
            response.status_code = 200
            return response

    return app
