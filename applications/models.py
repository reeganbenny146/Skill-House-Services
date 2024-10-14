from applications.database import db
from datetime import datetime


# class Services(db.Model):
#     __tablename__ = 'services'

#     id = db.Column(db.Integer, primary_key = True, nullable=False)
#     name = db.Column(db.String(30), nullable = False)
#     description = db.Column(db.String(100), nullable = False)
#     basePrice = db.Column(db.Integer, nullable= False)
#     # professionalList = db.relationship("Professionals", backref = "services", lazy = True, )


# class Users(db.Model):
#     __tablename__ = "users"

#     id = db.Column(db.Integer, primary_key = True, autoincrement = True)
#     email = db.Column(db.String(20), unique = True, nullable = False)
#     password = db.Column(db.String(20), nullable = False)
#     role = db.Column(db.String(10), nullable = False) 

#     __mapper_args__ = {
#         'polymorphic_on': role,
#         'polymorphic_identity': 'users'
#     }

# class Customers(Users):
#     __tablename__ = 'customers'

#     id = db.Column(db.Integer, primary_key = True)
#     userId = db.Column(db.Integer, db.ForeignKey('users.id'))
#     name = db.Column(db.String(20), nullable = False)
#     mobileNo = db.Column(db.String(10), nullable = False)
#     address = db.Column(db.String(100), nullable = False)
#     pinCode = db.Column(db.Integer, nullable = False)

#     __mapper_args__ = {
#         'polymorphic_identity': 'customer'
#     }

# class Professionals(Users):
#     __tablename__ = 'professionals'

#     id = db.Column(db.Integer, primary_key = True)
#     userId = db.Column(db.Integer, db.ForeignKey('users.id'))
#     name = db.Column(db.String(20), nullable= False)
#     serviceId = db.Column(db.Integer, db.ForeignKey('services.id'), nullable= False)
#     experience = db.Column(db.Integer, nullable= False)
#     createdDate = db.Column(db.Date, default= datetime.utcnow, nullable = False)
#     resumePath = db.Column(db.String(100), nullable = False)
#     mobileNo = db.Column(db.String(10), nullable = False)
#     address = db.Column(db.String(100), nullable = False)
#     pinCode = db.Column(db.Integer, nullable = False)
#     incentive = db.Column(db.Integer, nullable = True)
#     status = db.Column(db.Integer, default = 0)

#     __mapper_args__ = {
#         'polymorphic_identity': 'professional'
#     }

# class Admin(Users):
#     __tablename__ = 'admin'

#     id = db.Column(db.Integer, primary_key= True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

#     __mapper_args__ = {
#         'polymorphic_identity': 'admin'
#     }



# class ServiceHistory(db.Model):
#     __tablename__ = 'serviceHistory'

#     id = db.Column(db.Integer, primary_key = True, nullable=False)
#     dateRequested = db.Column(db.Date, default= datetime.utcnow, nullable = False)
#     dateAccepted = db.Column(db.Date, nullable = False)
#     dateCompleted = db.Column(db.Date, nullable = False)
#     customerId = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable= False)
#     servicesId = db.Column(db.Integer, db.ForeignKey('services.id'), nullable= False)
#     professionalId = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable = False)
#     status = db.Column(db.Integer, nullable = False, default = 0)




class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    role = db.Column(db.String(10), nullable = False,default= 'admin') 

    customerList = db.relationship('Customers', backref = 'users', lazy =True, uselist = False)
    professionalList = db.relationship('Professionals', backref = 'users', lazy =True, uselist = False)

class Customers(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(20), nullable = False)
    mobileNo = db.Column(db.String(10), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    pinCode = db.Column(db.Integer, nullable = False)

    serviceHistoryList = db.relationship('ServiceHistory', backref= 'customers', lazy= True)



class Professionals(db.Model):
    __tablename__ = 'professionals'

    id = db.Column(db.Integer, primary_key = True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(20), nullable= False)
    serviceId = db.Column(db.Integer, db.ForeignKey('services.id'), nullable= False)
    experience = db.Column(db.Integer, nullable= False)
    createdDate = db.Column(db.Date, default= datetime.now(), nullable = False)
    resumePath = db.Column(db.String(100), nullable = False)
    mobileNo = db.Column(db.String(10), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    pinCode = db.Column(db.Integer, nullable = False)
    incentive = db.Column(db.Integer, nullable = True)
    status = db.Column(db.Integer, default = 0)

    serviceHistoryList = db.relationship("ServiceHistory", backref= 'professionals', lazy = True)


class ServiceHistory(db.Model):
    __tablename__ = 'serviceHistory'

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    dateRequested = db.Column(db.Date, default= datetime.now(), nullable = False)
    dateAccepted = db.Column(db.Date, nullable = False)
    dateCompleted = db.Column(db.Date, nullable = False)
    customerId = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable= False)
    servicesId = db.Column(db.Integer, db.ForeignKey('services.id'), nullable= False)
    professionalId = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable = False)
    status = db.Column(db.Integer, nullable = False, default = 0)


class Services(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key = True, nullable=False)
    name = db.Column(db.String(30), nullable = False)
    description = db.Column(db.String(100), nullable = False)
    basePrice = db.Column(db.Integer, nullable= False)

    professionalList = db.relationship("Professionals", backref = "services", lazy = True)
    serviceHistoryList = db.relationship("ServiceHistory", backref = "services", lazy = True)
