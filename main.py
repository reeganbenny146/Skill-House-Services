from flask import Flask, url_for, flash,redirect, request, jsonify
from flask_restful import Api, Resource
from flask_login import LoginManager
from applications.models import Users
from applications.database import db
from applications.config import Config
from applications.uploadDummyData import addAdminDetails
from applications.apiRoutes import initializeUserRoutes
import traceback

loginManger = LoginManager()

def create_app():
    try:
        app = Flask(__name__,template_folder='template',static_folder='static')
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        app.config.from_object(Config)

        db.init_app(app)
        loginManger.init_app(app)

        loginManger.login_view = 'login'
        with app.app_context():
            db.create_all()

            addAdminDetails()
        return app
    except Exception as e:
        print("{exception_type}: {exception_message}")
        return None

app = create_app()

api = Api(app)
initializeUserRoutes(api)

# Loading logged In user
@loginManger.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

from applications.routes import *




@loginManger.unauthorized_handler
def unauthorized():
    flash(('You need to log in first to access this page.', 'danger')) 
    return redirect(url_for('login')) 

from applications.utils import Colors

@app.errorhandler(Exception)
def page_not_found(error):
    error_details = traceback.format_exc()

    # Get the URL that caused the error
    requested_url = request.url

    # Log the error details to console
    print(f"{Colors.RED}Error Details: {error_details}")
    print(f"{Colors.YELLOW}Requested URL: {requested_url}")
    print(f"{Colors.RED}Error Summary: {str(error)}{Colors.RESET}")
    return redirect(url_for('error'))

if __name__ == '__main__':
    app.run(debug=True)