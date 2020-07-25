from flask import jsonify, request, Response
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.items import Items
from utils.error_handling import forbidden

class ItemsController(Resource):
    """
    Flask-resftul resource for returning db.item collection.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from app import default_config
    # Create flask app, config, and resftul api, then add ItemsController route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(ItemsController, '/item/')
    """
    @jwt_required
    def get(self):
        # pylint: disable=no-member
        output = Items.objects()
        return jsonify({'result': output})

    @jwt_required
    def post(self) -> Response:
        """
        POST response method for creating item.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)
        :return: JSON object
        """
        authorized: bool = Items.objects.get(id=get_jwt_identity()).access.admin

        if authorized:
            data = request.get_json()
            post_user = Items(**data).save()
            output = {'id': str(post_user.id)}
            return jsonify({'result': output})
        else:
            return forbidden()

class ItemController(Resource):
    """
    Flask-resftul resource for returning db.item collection.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from app import default_config
    # Create flask app, config, and resftul api, then add ItemApi route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(ItemApi, '/item/<item_id>')
    """
    @jwt_required
    def get(self, item_id: str) -> Response:
        """
        GET response method for single documents in item collection.
        :return: JSON object
        """
        output = Items.objects.get(id=item_id)
        return jsonify({'result': output})

    @jwt_required
    def put(self, item_id: str) -> Response:
        """
        PUT response method for updating a item.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)
        :return: JSON object
        """
        data = request.get_json()
        put_user = Items.objects(id=item_id).update(**data)
        return jsonify({'result': put_user})

    @jwt_required
    def delete(self, user_id: str) -> Response:
        """
        DELETE response method for deleting single item.
        JSON Web Token is required.
        Authorization is required: Access(admin=true)
        :return: JSON object
        """
        authorized: bool = Items.objects.get(id=get_jwt_identity()).access.admin

        if authorized:
            output = Items.objects(id=user_id).delete()
            return jsonify({'result': output})
        else:
            return forbidden()