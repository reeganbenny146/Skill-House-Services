from applications.database import db
from datetime import datetime
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(40), unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    role = db.Column(db.String(10), nullable = False) # [admin, professional, customer]
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete
    is_blocked = db.Column(db.Boolean, default = False, nullable = False) # to block Cients and Professional
    is_rejected = db.Column(db.Boolean, default = False, nullable = False) # to reject a profesional
    is_approved = db.Column(db.Boolean, default = True, nullable = False) # for professional default will be False
    customerDetails = db.relationship('Customers', backref = 'user', lazy =True, uselist = False)
    professionalDetails = db.relationship('Professionals', backref = 'user', lazy =True, uselist = False)
    adminDetails = db.relationship('Admin', backref = 'user', lazy =True, uselist = False)

    def soft_delete(self):
        self.is_deleted = True

    def updateBlock(self):
        self.is_blocked = not self.is_blocked

    def updateReject(self):
        self.is_rejected = not self.is_rejected

    def updateApprove(self):
        self.is_approved = not self.is_approved
        if self.is_rejected:
            self.is_rejected = not self.is_rejected

    @staticmethod
    def get_active_users():
        return Users.query.filter_by(is_deleted = False).all()

class Admin(db.Model, UserMixin):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    fname = db.Column(db.String(20), nullable = False)
    lname = db.Column(db.String(20), nullable = False)
    profilePhotoPath = db.Column(db.String(20), default="../static/images/users/default-admin.jpg",nullable= False)


class Customers(db.Model, UserMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    fname = db.Column(db.String(20), nullable = False)
    lname = db.Column(db.String(20), nullable = False)
    profilePhotoPath = db.Column(db.String(20), default="../static/images/users/default-user.jpg",nullable= False)
    mobileNo = db.Column(db.String(10), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    pinCode = db.Column(db.Integer, nullable = False)
    is_blocked = db.Column(db.Boolean, default = False, nullable = False)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete

    serviceHistoryList = db.relationship('ServiceHistory', primaryjoin="and_(ServiceHistory.customerId == Customers.id, ServiceHistory.is_deleted == False)", backref= 'customer', lazy= True)

    def updateBlock(self):
        self.is_blocked = not self.is_blocked
        self.user.updateBlock()

    def soft_delete(self):
        self.is_deleted = True
        self.user.soft_delete()

    @staticmethod
    def get_all_customers():
        return Customers.query.filter_by(is_deleted=False)
    
    @staticmethod
    def get_active_customers():
        return Customers.query.filter_by(is_deleted=False, is_blocked = False )


class Professionals(db.Model, UserMixin):
    __tablename__ = 'professionals'

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'))
    fname = db.Column(db.String(20), nullable= False)
    lname = db.Column(db.String(20), nullable= False)
    profilePhotoPath = db.Column(db.String(20), default="../static/images/users/default-user.jpg",nullable= False)
    serviceId = db.Column(db.Integer, db.ForeignKey('services.id'), nullable= False)
    experience = db.Column(db.Integer, nullable= False)
    createdDate = db.Column(db.Date, default= datetime.now(), nullable = False)
    resumePath = db.Column(db.String(100), nullable = False)
    mobileNo = db.Column(db.String(10), nullable = False)
    address = db.Column(db.String(100), nullable = False)
    pinCode = db.Column(db.Integer, nullable = False)
    incentive = db.Column(db.Integer, default = 0 , nullable = True)
    is_approved = db.Column(db.Boolean, default = False, nullable = False)
    is_blocked = db.Column(db.Boolean, default = False, nullable = False)
    is_rejected = db.Column(db.Boolean, default = False, nullable = False)
    is_serviceAvailable = db.Column(db.Boolean, default = True, nullable = False)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete

    serviceHistoryList = db.relationship("ServiceHistory", backref= 'professional', lazy = True)

    def soft_delete(self):
        self.is_deleted = True
        self.user.soft_delete()

    @staticmethod
    def get_active_professionals():
        return Professionals.query.filter_by(is_deleted=False, is_approved = True, is_blocked = False, is_rejected = False, is_serviceAvailable = True  )
    
    @staticmethod
    def get_all_professionals():
        return Professionals.query.filter_by(is_deleted=False)

    def updateBlock(self):
        self.is_blocked = not self.is_blocked
        self.user.updateBlock()

    def updateReject(self):
        self.is_rejected = not self.is_rejected
        self.user.updateReject()
    
    def updateApprove(self):
        self.is_approved = not self.is_approved
        if self.is_rejected:
            self.is_rejected = not self.is_rejected
        self.user.updateApprove()

    def updateServiceAvailable(self):
        self.is_serviceAvailable = not self.is_serviceAvailable


class Services(db.Model, UserMixin):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    name = db.Column(db.String(30), nullable = False)
    categoryId = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable = False)
    description = db.Column(db.String(100), nullable = False)
    basePrice = db.Column(db.Integer, nullable= False)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete

    professionals = db.relationship("Professionals", primaryjoin="and_(Professionals.serviceId == Services.id, Professionals.is_deleted == False)", backref = "service", lazy = True)
    serviceHistory = db.relationship("ServiceHistory", backref = "service", lazy = True)

    def soft_delete(self):
        self.is_deleted = True
        print(self.professionals)
        for professional in self.professionals:
            professional.updateServiceAvailable()

    @staticmethod
    def get_active_services():
        return Services.query.filter_by(is_deleted=False)
    
    @staticmethod
    def get_active_services_byId(categoryId= None):
        query = Services.query.filter_by(is_deleted=False)
        if categoryId is not None:
            query = query.filter_by(categoryId=categoryId)
        return query



class Categories(db.Model, UserMixin):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    name = db.Column(db.Integer, nullable = False)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete

    services = db.relationship("Services", primaryjoin="and_(Services.categoryId == Categories.id, Services.is_deleted == False)", backref = "category" , lazy = True)

    def soft_delete(self):
        self.is_deleted = True
        for service in self.services:
            service.soft_delete()

    @staticmethod
    def get_active_categories():
        return Categories.query.filter_by(is_deleted=False)

class ServiceHistory(db.Model, UserMixin):
    __tablename__ = 'serviceHistory'

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    dateRequested = db.Column(db.Date, default= datetime.now(), nullable = False)
    dateAccepted = db.Column(db.Date, nullable = True)
    dateCompleted = db.Column(db.Date, nullable = True)
    customerId = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable= False)
    servicesId = db.Column(db.Integer, db.ForeignKey('services.id'), nullable= False)
    professionalId = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable = True)
    reviewsId = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable = True)
    status = db.Column(db.Integer, nullable = False, default = 0) # 0 - Pending, 1 - Accepted, 2 - Completed by professional, 3 - Closed(Only after finalization of client and professioanal) 4- Rejected  5- Deleted
    is_requested = db.Column(db.Boolean, default = False, nullable = False) # to request a service directly to a professional (Update by client)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete

    def soft_delete(self):
        self.is_deleted = True

    # Returns a query object of service History
    @staticmethod
    def get_active_serviceHistory():
        return ServiceHistory.query.filter_by(is_deleted=False) # returns a query

class Reviews(db.Model, UserMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key = True, nullable=False, autoincrement = True)
    rating = db.Column(db.Integer, nullable = False)
    reviewText = db.Column(db.String(200), nullable = False)
    is_deleted = db.Column(db.Boolean, default = False, nullable = False) # For Soft Delete

    serviceHistory = db.relationship("ServiceHistory", backref = "reviews" , lazy= True, uselist = False)


