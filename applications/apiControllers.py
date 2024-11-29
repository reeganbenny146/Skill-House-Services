from flask_restful import Resource, reqparse
from applications.models import Users, Professionals, Customers, Services
import os
from applications.database import db


user_parser = reqparse.RequestParser()
user_parser.add_argument("firstName", type=str, required=True, help="firstName is required")
user_parser.add_argument("lastName", type=str, required=True, help="lastName is required")
user_parser.add_argument("username", type=str, required=True, help="Username is required")
user_parser.add_argument("profileImage", type=str, required=True, help="profileImage is required")
user_parser.add_argument("email", type=str, required=True, help="Email is required")
user_parser.add_argument("password", type=str, required=True, help="Password is required")
user_parser.add_argument("cpassword", type=str, required=True, help="Confirm Password is required")
user_parser.add_argument("address", type=str, required=True, help="address is required")
user_parser.add_argument("mobileNumber", type=int, required=True, help="mobileNumber is required")
user_parser.add_argument("pincode", type=int, required=True, help="pincode is required")
user_parser.add_argument("role", type=str, required=True, help="role is required")
user_parser.add_argument("experience", type=str, required=False, help="Experience (for professional users)")
user_parser.add_argument("serviceType", type=int, required=False, help="Service Type (for professional users)")
user_parser.add_argument("incentive", type=int, required=False, help="Incentive (for professional users)")
user_parser.add_argument("resume", type=str, required=False, help="Resume (for professional users)")



class RegisterController(Resource):
    def post(self):
        args = user_parser.parse_args()
        try:
            fname = args['firstName']
            lname = args['lastName']
            username = args['username']
            profilePhotoPath = args['profileImage']
            email = args['email']
            password = args['password']
            cpassword = args['cpassword']
            address = args['address']
            mob = args['mobileNumber']
            pin = args['pincode']
            role = args['role']

            if role not in ['client','professional']:
                return {"message": "User should select a valid role."}, 400
            
            if any(not field for field in [fname, lname, username, email, password, cpassword, address, mob, pin]):
                return {"message": "User should enter all values."}, 400

            check_user = Users.query.filter_by(username = username).first()
            if check_user:
                return {"message": "User with given username already in database."}, 400
            else:
                import re
                username_regex = r"^[a-zA-Z0-9]{3,30}$"
                if not re.match(username_regex, username):
                    return {"message": "Username must be 3-30 characters long, contain only letters, numbers and start with a letter!."}, 400
            
            user = Users.query.filter_by(email=email).first()
            if user:
                return {"message": "User with given email already in database."}, 400

            elif password != cpassword:
                return {"message": "Password doesn't match. Please try again!"}, 400

            if role == "professional":
                professional_args = user_parser.parse_args()
                experience = args['experience']
                serviceId = args['serviceType']
                incentive = args['incentive']
                resumePath = args['resume']

                if not experience:
                    return {"message": "Professional should add experience."}, 400
                if not resumePath:
                    return {"message": "Professional should add resume."}, 400
                
                service = Services.query.get(serviceId)
                professional = Professionals(fname= fname,
                                            lname = lname,
                                            profilePhotoPath = profilePhotoPath,
                                            experience = experience,
                                            resumePath= resumePath,
                                            mobileNo = mob,
                                            address = address,
                                            pinCode = int(pin),
                                            incentive = int(incentive),
                                            service = service
                                            )
                user = Users(email = email,
                            username = username,
                            password = password,
                            role = role,
                            is_approved = False,
                            professionalDetails = professional) 
                
                db.session.add(user)
                db.session.commit()
                return {"message": "User registered successfully"}, 201

            elif role == "client":
                customer = Customers(
                    fname = fname,
                    lname = lname,
                    mobileNo = mob,
                    profilePhotoPath = profilePhotoPath,
                    address = address,
                    pinCode = int(pin)
                )

                user = Users(email = email,
                            username = username,
                            password = password,
                            role = role,
                            customerDetails = customer)  
                db.session.add(user)
                db.session.commit()
                return {"message": "User registered successfully"}, 201


        except Exception as e:
            db.session.rollback()
            print(e)
            return {"message": "Error Occured."}, 500
        

deleteUser_parser = reqparse.RequestParser()
# mention professional Id or customer Id
deleteUser_parser.add_argument("userId", type=int, required=True, help="UserId is required") 
deleteUser_parser.add_argument("role", type=str, required=True, help="Role is required") 

class deleteUserController(Resource):
    def put(self):
        try:
            args = deleteUser_parser.parse_args()
            role = args['role']
            if role == 'client':
                customerId = args['userId']
                customer = Customers.query.get(customerId)
                customer.soft_delete()
                db.session.commit()
                return {"message": "customer successfully soft deleted!"}, 201
            elif role== 'professional':
                professionalId = args['userId']
                professional = Professionals.query.get(professionalId)
                professional.soft_delete()
                db.session.commit()
                return {"message": "Professional successfully soft deleted!"}, 201
            else:
                return {"message": "Invalid role!"}, 400
        except Exception as e:
            db.session.rollback()
            print(e)
            return {"message": "Error Occured."}, 500
        
    def delete(self):
        args = deleteUser_parser.parse_args()
        try:
            role = args['role']
            if role == 'client':
                customerId = args['userId']
                customer = Customers.query.get(customerId)
                userId = customer.user.id
                user = Users.query.get(userId)
                db.session.delete(customer)
                db.session.delete(user)
                db.session.commit()
                return {"message": "customer successfully deleted!"}, 201
            elif role== 'professional':
                professionalId = args['userId']
                professional = Professionals.query.get(professionalId)
                userId = professional.user.id
                user = Users.query.get(userId)
                db.session.delete(professional)
                db.session.delete(user)
                db.session.commit()
                return {"message": "Professional successfully deleted!"}, 201
            else:
                return {"message": "Invalid role!"}, 400
        except Exception as e:
            db.session.rollback()
            print(e)
            return {"message": "Error Occured."}, 500
