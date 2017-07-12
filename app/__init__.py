from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import request, jsonify, abort, url_for
from functools import wraps
from flask_bcrypt import Bcrypt
from instance.config import app_config


db = SQLAlchemy()
validation_schema = Marshmallow()

from app.models import User, UserSchema, BucketlistSchema, ItemSchema


def create_app(config_name):
    """This function creates the actual application to be used and consumed
    within the API"""
    from app.models import Bucketlist, Item
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

    @app.errorhandler(405)
    def invalid_method(e):
        response = jsonify({"error": "Method not allowed"})
        response.status_code = 405
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
                    response = jsonify({"msg": "Access denied."})
                    response.status_code = 401
                    return response
            else:
                response = jsonify({"msg": "Access denied."})
                response.status_code = 401
                return response
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
                response.status_code = 409
                return response
            if email:
                if User.query.filter_by(email=email).first():
                    response = jsonify({'msg': "Email already in use"})
                    response.status_code = 409
                    return response
                if password:
                    errors = UserSchema().validate({"username": username,
                                                    "email": email,
                                                    "password": password},
                                                   partial=True)
                    if errors:
                        return jsonify(errors), 400
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
                    response.status_code = 400
                    return response
            else:
                response = jsonify({'msg':
                                    "User must have an email"})
                response.status_code = 400
                return response
        else:
            response = jsonify({'msg':
                                "User must have a username"})
            response.status_code = 400
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
                return errors, 400

        else:
            response = jsonify({
                            "msg": "Username and password must be provided"})
            response.status_code = 400
            return response
        user = User.query.filter_by(username=username).first()
        if user:
            if Bcrypt().check_password_hash(user.password, password):
                access_token = User.create_access_token(user.id)
                return jsonify({"msg": "Login successful",
                                "token": access_token.decode()})
            else:
                response = jsonify({"msg": "Username or password invalid."})
                response.status_code = 401
                return response
        else:
            response = jsonify({"msg": "Username and password invalid."})
            response.status_code = 401
            return response

    @app.route('/api/v1/bucketlists', methods=['POST', 'GET'])
    @check_token
    def bucketlists():
        """This function does the actual creation of the bucketlist within the
        API"""
        if request.headers.get("Authorization"):
            token = bytes(request.headers.get("Authorization").
                          split(" ")[1], "utf-8")
            user_id = User.decode_access_token(token)
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                errors = BucketlistSchema().validate({"name": name})
                if errors:
                    return errors, 400
                bucketlist = Bucketlist(name=name, creator=user_id)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'creator': bucketlist.creator,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
                response.status_code = 201
                return response
            else:
                response = jsonify({"msg": "Bucketlist must have a name"})
                response.status_code = 400
                return response
        else:
            # GET
            page_no = request.args.get('page_no', 1)
            limit = request.args.get('limit', 20)
            q = request.args.get('q', "")

            bucketlists = Bucketlist.query.filter_by(creator=user_id).filter(
                Bucketlist.name.like('%{}%'.format(q))).paginate(int(page_no),
                                                                 int(limit))
            if not bucketlists:
                abort(404)

            results = []

            for bucketlist in bucketlists.items:
                obj = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                results.append(obj)
            previous = {'prev': url_for(request.endpoint, page_no=bucketlists.
                                        prev_num, limit=limit, _external=True)
                        if bucketlists.has_prev else None}
            nxt = {'next': url_for(request.endpoint, page_no=bucketlists.
                                   next_num, limit=limit, _external=True)
                   if bucketlists.has_next else None}
            results.append(previous)
            results.append(nxt)
            if len(results) < 1:
                results = {'msg': "There are no bucketlists in the system"}
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/api/v1/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE']
               )
    @check_token
    def bucketlist_management(id, **kwargs):
        """This function handles all the management functions of the bucketlist
        """
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            abort(404)

        if request.method == 'DELETE':
            bucketlist.delete()
            return {"message": "The bucketlist {} has been successfully deleted"
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
            items = Item.query.filter_by(bucketlist_owner=id)
            itemlist = []

            for item in items:
                obj = {
                    'id': item.id,
                    'item_name': item.name,
                    'date_created': item.date_created,
                    'date_modified': item.date_modified,
                    'done': item.done
                }
                itemlist.append(obj)
            if len(itemlist) < 1:
                itemlist = "No items to display"
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'items': itemlist,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified})
            response.status_code = 200
            return response

    @app.route('/api/v1/bucketlists/<int:id>/items', methods=['POST', 'GET'])
    @check_token
    def item_creation(id, *kwargs):
        """This function does the actual creation of the item within the
        bucketlist"""
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                errors = ItemSchema().validate({"name": name})
                if errors:
                    return errors, 400
                else:
                    if Item.query.filter_by(name=name).first():
                        response = jsonify({"msg": "Item already in bucketlist"})
                        response.status_code = 409
                        return response
                    else:
                        item = Item(name=name, bucketlist_owner=id)
                        item.save()
                        response = jsonify({
                            'id': item.id,
                            'bucketlist_owner': id,
                            'item_name': item.name,
                            'date_created': item.date_created,
                            'date_modified': item.date_modified,
                            'done': item.done
                        })
                        response.status_code = 201
                        return response
            else:
                response = jsonify({"msg": "Item must have a name"})
                response.status_code = 400
                return response

        else:
            response = jsonify({"msg": "Method not allowed"})
            response.status_code = 405
            return response

    @app.route('/api/v1/bucketlists/<int:bucketlist_id>/items/<int:item_id>',
               methods=['GET', 'PUT', 'DELETE'])
    @check_token
    def item_manipulation(bucketlist_id, item_id, *kwargs):
        """This functions covers all the manipulation operations concerning
        items"""
        bucketlist = Bucketlist.query.filter_by(id=bucketlist_id).first()
        if not bucketlist:
            abort(404)

        item = Item.query.filter_by(id=item_id).first()
        if not item:
            abort(404)

        if request.method == 'DELETE':
            item.delete()
            return {"message": "The item {} has been successfully deleted"
                    .format(item.id)}, 200

        elif request.method == 'PUT':
            name = str(request.data.get('name', ''))
            done = str(request.data.get('done', ''))
            if not name and done:
                response = jsonify({"msg": """Name and whether done or not
                                    required"""})
                response.status_code = 400
                return response
            item.name = name
            item.done = done
            item.save()
            response = jsonify({
                'id': item.id,
                'name': item.name,
                'date_created': item.date_created,
                'date_modified': item.date_modified,
                'done': item.done,
                'msg': "Item update success"})
            response.status_code = 200
            return response

    return app
