from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from applications.database import db
from applications.config import Config
from applications.models import *


def create_app():
    try:
        app = Flask(__name__,template_folder='template',static_folder='static')
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
        app.config.from_object(Config)

        db.init_app(app)

        with app.app_context():
            db.create_all()
            
        return app
    except Exception as e:
        print("{exception_type}: {exception_message}")

app = create_app()


from applications.routes import *

api = Api(app)



@app.errorhandler(Exception)
def page_not_found(error):
    print('error: '+str(error))
    return redirect(url_for('error'))

if __name__ == '__main__':
    app.run(debug=True)