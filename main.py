from flask import Flask, render_template, session
from applications.database import db
from applications.config import Config
from applications.models import *


def create_app():
    app = Flask(__name__,template_folder='template')
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()
        
    return app

app = create_app()


from applications.routes import *



if __name__ == '__main__':
    app.run(debug=True)