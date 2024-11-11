from flask import Flask, url_for, flash,redirect, request, jsonify
from flask_restful import Api, Resource
from flask_login import LoginManager
from applications.models import Users
from applications.database import db
from applications.config import Config

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
            
        return app
    except Exception as e:
        print("{exception_type}: {exception_message}")

app = create_app()

# Loading logged In user
@loginManger.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

from applications.routes import *

api = Api(app)


@loginManger.unauthorized_handler
def unauthorized():
    flash(('You need to log in first to access this page.', 'danger')) 
    return redirect(url_for('login')) 

@app.errorhandler(Exception)
def page_not_found(error):
    print(f"error: {str(error)}")
    return redirect(url_for('error'))

if __name__ == '__main__':
    app.run(debug=True)