from applications.database import db
from datetime import datetime
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    email = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    role = db.Column(db.String(10), nullable = False) # [admin, professional, customer]
    status = db.Column(db.Integer, nullable=False, default= 0) # 0 - Pending, 1 - Approved, 2 - rejected
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete
    customerDetails = db.relationship('Customers', backref = 'user', lazy =True, uselist = False)
    professionalDetails = db.relationship('Professionals', backref = 'user', lazy =True, uselist = False)
    adminDetails = db.relationship('Admin', backref = 'user', lazy =True, uselist = False)

    def soft_delete(self):
        self.is_deleted = True

    @staticmethod
    def get_active_users():
        return Users.query.filter_by(is_deleted = False).all()

class Admin(db.Model, UserMixin):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    fname = db.Column(db.String(20), nullable = False)
    lname = db.Column(db.String(20), nullable = False)
    profilePhotoPath = db.Column(db.String(20), default="static/images/default-admin.jpg",nullable= False)


class Customers(db.Model, UserMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    fname = db.Column(db.String(20), nullable = False)
    lname = db.Column(db.String(20), nullable = False)
    profilePhotoPath = db.Column(db.String(20), default="static/images/default-user.jpg",nullable= False)
    mobileNo = db.Column(db.String(10), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    pinCode = db.Column(db.Integer, nullable = False)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete

    serviceHistoryList = db.relationship('ServiceHistory', backref= 'customers', lazy= True)



class Professionals(db.Model, UserMixin):
    __tablename__ = 'professionals'

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    fname = db.Column(db.String(20), nullable= False)
    lname = db.Column(db.String(20), nullable= False)
    profilePhotoPath = db.Column(db.String(20), default="static/images/default-user.jpg",nullable= False)
    serviceId = db.Column(db.Integer, db.ForeignKey('services.id'), nullable= False)
    experience = db.Column(db.Integer, nullable= False)
    createdDate = db.Column(db.Date, default= datetime.now(), nullable = False)
    resumePath = db.Column(db.String(100), nullable = False)
    mobileNo = db.Column(db.String(10), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    pinCode = db.Column(db.Integer, nullable = False)
    incentive = db.Column(db.Integer, nullable = True)
    status = db.Column(db.Integer, default = 0) # 0 - Pending , 1 - Approved, 2 - Blocked, 3 - Deleted
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete

    serviceHistoryList = db.relationship("ServiceHistory", backref= 'professionals', lazy = True)

    def soft_delete(self):
        self.is_deleted = True

        self.user.soft_delete()


class Services(db.Model, UserMixin):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    name = db.Column(db.String(30), nullable = False)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    description = db.Column(db.String(100), nullable = False)
    basePrice = db.Column(db.Integer, nullable= False)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete

    professionals = db.relationship("Professionals", backref = "services", lazy = True)
    serviceHistoryList = db.relationship("ServiceHistory", backref = "services", lazy = True)

    def soft_delete(self):
        self.is_deleted = True

        for professional in self.professionals:
            professional.soft_delete()

    @staticmethod
    def get_active_services():
        return Services.query.filter_by(is_deleted=False).all()


class Categories(db.Model, UserMixin):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    name = db.Column(db.Integer, nullable = False, unique = True)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete

    services = db.relationship("Services", backref = "category" , lazy = True)

    def soft_delete(self):
        self.is_deleted = True
        for service in self.services:
            service.soft_delete()

    @staticmethod
    def get_active_categories():
        return Categories.query.filter_by(is_deleted=False).all()

class ServiceHistory(db.Model, UserMixin):
    __tablename__ = 'serviceHistory'

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    dateRequested = db.Column(db.Date, default= datetime.now(), nullable = False)
    dateAccepted = db.Column(db.Date, nullable = False)
    dateCompleted = db.Column(db.Date, nullable = False)
    customerId = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable= False)
    servicesId = db.Column(db.Integer, db.ForeignKey('services.id'), nullable= False)
    professionalId = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable = True)
    reviewsId = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable = True)
    status = db.Column(db.Integer, nullable = False, default = 0) # 0 - pending, 1 - Accepted, 2 - Completed 
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete


class Reviews(db.Model, UserMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    customerId = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable= False)
    professionalId = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable = False)
    rating = db.Column(db.Integer, nullable = False)
    reviewText = db.Column(db.String(200), nullable = False)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete

    serviceHistory = db.relationship("ServiceHistory", backref = "reviews" , lazy= True, uselist = False)






