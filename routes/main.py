from controllers.items import ItemsController, ItemController
from controllers.users import UsersController, UserController
from controllers.auth import LoginController, SignUpController, WelcomeController


def get_routes(api):
    api.add_resource(WelcomeController, '/')

    api.add_resource(SignUpController, '/api/v1/register')
    api.add_resource(LoginController, '/api/v1/login')

    api.add_resource(UsersController, '/api/v1/user')
    api.add_resource(UserController, '/api/v1/user/<user_id>')

    api.add_resource(ItemsController, '/api/v1/item')
    api.add_resource(ItemController, '/api/v1/item/<item_id>')