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

        # admin_role = Role.query.filter_by(name='admin').first()
        # if not admin_role:
        #     admin_role = Role(name='admin')
        #     db.session.add(admin_role)

        # cust_role = Role.query.filter_by(name='customer').first()
        # if not cust_role:
        #     cust_role = Role(name='customer')
        #     db.session.add(cust_role)

        # store_manager = Role.query.filter_by(name='store_manager').first()
        # if not store_manager:
        #     store_manager = Role(name  ='store_manager')
        #     db.session.add(store_manager)
        
        # admin = User.query.filter_by(username='admin').first()
        # if not admin:
        #     admin = User(username='admin',
        #                  email = 'admin@abc.com',
        #                 password = 'admin',
        #                 roles= [admin_role,store_manager])
        #     db.session.add(admin)

        # db.session.commit()
        


    return app

app = create_app()

@app.route('/')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)