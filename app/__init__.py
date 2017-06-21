from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort
from instance.config import app_config


db = SQLAlchemy()

from app.models import User

def create_app(config_name):
    """This function creates the actual application to be used and consumed
    within the API"""
    from app.models import Bucketlist
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/auth/register', methods=['POST'])
    def register():
        """This function registers the user who will create the bucketlists"""
        name = str(request.data.get('name', ''))
        if name:
            user = User(name=name)
            user.save()
            response = jsonify({'msg':  "User has been created successfully"})
            response.status_code = 201
            return response

    @app.route('/bucketlists/', methods=['POST', 'GET'])
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
            response = jsonify(results)
            response.status_code = 200
            return response

    @app.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
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
