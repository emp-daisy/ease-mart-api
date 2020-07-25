from flask import Response, request, jsonify
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from models.users import Users
from utils.error_handling import unauthorized
import datetime

class SignUpController(Resource):
    """
    Flask-resftul resource for creating new user.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from app import default_config
    # Create flask app, config, and resftul api, then add SignUpController route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(SignUpController, '/api/v1/register')
    """
    @staticmethod
    def post() -> Response:
        """
        POST response method for creating user.
        :return: JSON object
        """
        data = request.get_json()
        post_user = Users(**data)
        post_user.save()
        output = {'id': str(post_user.id)}
        return jsonify({'result': output})


class LoginController(Resource):
    """
    Flask-resftul resource for retrieving user web token.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from app import default_config
    # Create flask app, config, and resftul api, then add LoginController route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(LoginController, '/api/v1/login')
    """
    @staticmethod
    def post() -> Response:
        """
        POST response method for retrieving user web token.
        :return: JSON object
        """
        data = request.get_json()
        user = Users.objects.get(email=data.get('email'))
        auth_success = user.check_hash(data.get('logon_key'))
        if not auth_success:
            return unauthorized()
        else:
            expiry = datetime.timedelta(days=5)
            access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
            refresh_token = create_refresh_token(identity=str(user.id))
            return jsonify({'result': {'access_token': access_token,
                                       'refresh_token': refresh_token,
                                       'logged_in_as': f"{user.email}"}})


class WelcomeController(Resource):
    """
    Flask-resftul resource for returning a welcome response.
    :Example:
    >>> from flask import Flask
    >>> from flask_restful import Api
    >>> from app import default_config
    # Create flask app, config, and resftul api, then add WelcomeController route
    >>> app = Flask(__name__)
    >>> app.config.update(default_config)
    >>> api = Api(app=app)
    >>> api.add_resource(WelcomeController, '/')
    """
    def get(self):
        return jsonify({'result': 'Welcome to Ease Mart API!'})