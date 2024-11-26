from main import app
from flask import render_template, session, url_for, redirect, request ,flash
from applications.models import *
from flask_login import login_user, logout_user, current_user, login_required
import os
from sqlalchemy import or_, and_
from datetime import datetime
from functools import wraps

# define decorator for active and inactive accounts
def active_account(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_blocked:
            return render_template('blocked.html', user = current_user) 
        
        if current_user.is_rejected:
            return render_template('reject.html', user = current_user)
        return func(*args, **kwargs)
    return wrapper

# User login routes
@app.route('/login', methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == "GET":
        if '_user_id' in session:
            session.pop('_user_id')
            session.clear()
        if 'reg_user_role' in session:
            session.pop('reg_user_role')
            session.clear()

        return render_template('login.html')
    else:
        email = request.form.get('email',None)
        password = request.form.get('password', None)
        if not email  or not password :
            flash(('Email and password must not empty..!!!','danger'))
            return redirect(url_for('login'))
        user = Users.query.filter_by(email=email).first()
        if not user:
            flash(('Please enter a valid email..!!!','danger'))
            return redirect(url_for('login'))
        elif user.is_deleted:
            flash((f'{user.email} was deleted by admin. Please contact admin(admin@gmail.com).!!!','danger'))
            return redirect(url_for('login'))
        # elif user.is_blocked:
        #     flash((f'{user.email} was blocked by admin. Please contact admin(admin@gmail.com).!!!','danger'))
        #     return redirect(url_for('login'))
        # elif user.is_rejected:
        #     flash((f'{user.email} application was rejected by admin. Please contact admin(admin@gmail.com).!!!','danger'))
        #     return redirect(url_for('login'))
        elif user.password == password:
            login_user(user)
            flash((user.email + ' have succesfully logged in!!', 'success'))
            return redirect(url_for('dashboard'))
        else:
            flash(('invalid password..!!!','danger'))
            return redirect(url_for('login'))

# User role select
@app.route('/role',methods = ["GET","POST"])
def role():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        return render_template('role.html')
    else:
        role = request.form.get("userType",None)
        if role:
            session['reg_user_role'] = role
            return redirect(url_for('registration'))
        else:
            flash(('Please select a role.','danger'))
            return redirect(url_for('role'))

# registration
@app.route('/registration',methods = ['GET', 'POST'])
def registration():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        if 'reg_user_role' not in session:
            flash(('Please select a role.','danger'))
            return redirect(url_for('role'))
        if request.method == "GET":
            categories = Categories.get_active_categories().all()
            return render_template('registration.html', categories = categories)
        else:
            fname = request.form.get('firstName')
            lname = request.form.get('lastName')
            username = request.form.get('username')
            image = request.files.get('profileImage',None)
            email = request.form.get('email')
            password = request.form.get('password')
            cpassword = request.form.get('cpassword')
            address = request.form.get('address')
            mob = request.form.get('mobileNumber')
            pin = request.form.get('pincode')
            role = session['reg_user_role']

            if role not in ['client','professional']:
                flash(('Please select a valid role.','danger'))
                return redirect(url_for('role'))
            
            if any(not field for field in [fname, lname, username, email, password, cpassword, address, mob, pin]):
                flash(('Please enter all field','danger'))
                return redirect(url_for('registration'))

            check_user = Users.query.filter_by(username = username).first()
            if check_user:
                flash(('username already exists..Try another username or login!', 'danger'))
                return redirect(url_for('registration'))
            else:
                import re
                username_regex = r"^[a-zA-Z0-9]{3,30}$"
                if not re.match(username_regex, username):
                    flash(('Username must be 3-30 characters long, contain only letters, numbers and start with a letter!', 'danger'))
                    return redirect(url_for('registration'))
            
            imageFilePath = None
            profilePhotoPath = ''
            if image:
                file_ext = os.path.splitext(image.filename)[1]
                new_filename = f"{username}{file_ext}"
                imageFilePath = 'images\\users\\' + new_filename
                profilePhotoPath = os.path.join('static', imageFilePath)
                os.makedirs(os.path.dirname(profilePhotoPath), exist_ok=True)
                image.save(profilePhotoPath)    
                profilePhotoPath = '../static/images/users/' + new_filename 

            user = Users.query.filter_by(email=email).first()
            if user:
                flash(('Email already exists..Try another email or login!', 'danger'))
                return redirect(url_for('registration'))
            elif password != cpassword:
                flash(('Password doesnot match.. Please try again..', 'danger'))
                return redirect(url_for('registration'))
            elif not role:
                flash(('Please set you role.. Please try again..', 'danger'))
                return redirect(url_for('registration'))  

            if role == "professional":
                experience = request.form.get('experience')
                serviceId = request.form.get('serviceType')
                incentive = request.form.get('incentive',0)
                resume = request.files.get('resume')

                if not experience:
                    flash(('Add your experience.. Please try again..', 'danger'))
                    return redirect(url_for('registration')) 
                if not resume:
                    flash(('Professional cannot login without a resume.. Please try again..', 'danger'))
                    return redirect(url_for('registration')) 
                resumeFilePath = None
                resumePath = ''
                if resume:
                    file_ext = os.path.splitext(resume.filename)[1]
                    new_resumeName = f"{username}{file_ext}"
                    resumeFilePath = 'documents\\users\\professionals\\resume\\' + new_resumeName
                    resumePath = os.path.join('static', resumeFilePath)
                    os.makedirs(os.path.dirname(resumePath), exist_ok=True)
                    resume.save(resumePath) 
                    resumePath = '../static/documents/users/professionals/resume/' + new_resumeName
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
                            role = session['reg_user_role'],
                            is_approved = False,
                            professionalDetails = professional) 
                
                db.session.add(user)
                db.session.commit()
                session.pop('reg_user_role',None)
                flash(("User(Professional) has successfully created.. Please login.","success"))
                return redirect(url_for('login'))

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
                            role = session['reg_user_role'],
                            customerDetails = customer)  
                db.session.add(user)
                db.session.commit()
                session.pop('reg_user_role',None)
                flash(("User(Client) has successfully created.. Please login.","success"))
                return redirect(url_for('login'))

    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('registration'))


# User dashboard
@app.route('/')
@login_required
@active_account
def dashboard():
    try:
        user = Users.query.get(current_user.id)
        if user.role == 'admin':
            categories = Categories.get_active_categories().all()
            services = Services.get_active_services().all()
            professionals = Professionals.get_all_professionals().all()
            serviceRequests = ServiceHistory.get_active_serviceHistory().all()
            customers = Customers.get_all_customers().all()
            return render_template('dashboard.html',user = user, categories = categories, services = services, professionals = professionals, serviceRequests = serviceRequests, customers = customers)
        elif user.role == 'client':
            categories = Categories.get_active_categories().all()
            services = Services.get_active_services().all()
            serviceRequests = ServiceHistory.get_active_serviceHistory().filter(ServiceHistory.customerId == user.customerDetails.id)
            serviceHistories = serviceRequests.all()
            activeServiceRequests = serviceRequests.filter(ServiceHistory.status.in_([0, 1, 2])).all()
            return render_template('dashboard.html',user = user, categories = categories, services = services, serviceHistories=serviceHistories, activeServiceRequests = activeServiceRequests)
        else:
            serviceRequests = ServiceHistory.get_active_serviceHistory()
            serviceHistories = serviceRequests.filter(ServiceHistory.professionalId == user.professionalDetails.id).all()
            activeServiceRequests = serviceRequests.filter(ServiceHistory.status.in_([1, 2]), ServiceHistory.professionalId == user.professionalDetails.id).all()
            newServiceRequests = serviceRequests.filter(and_(ServiceHistory.status == 0, ServiceHistory.is_requested == False), 
                                                                    and_(ServiceHistory.status == 0, ServiceHistory.is_requested == True, 
                                                                         ServiceHistory.professionalId == user.professionalDetails.id),  
                                                                         ServiceHistory.servicesId == user.professionalDetails.serviceId ).all()
            return render_template('dashboard.html',user= user, newServiceRequests = newServiceRequests, activeServiceRequests = activeServiceRequests, serviceHistories = serviceHistories)
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('logout'))

# Search Results
@app.route('/search-results',methods=['GET', 'POST'])
@login_required
@active_account
def search():
    try:
        user = Users.query.get(current_user.id)
        if(request.method == 'GET'):
            return render_template('searchResults.html',user = user)
        else:
            searchOption = request.form.get('searchOption')
            searchText = request.form.get('searchText')
            if user.role == 'admin':
                if searchOption == 'Categories':
                    categories = Categories.get_active_categories().filter(Categories.name.ilike(f'%{searchText}%')).all()
                    categoryIds = [category.id for category in categories]
                    if categoryIds:
                        services = Services.get_active_services().filter(Services.categoryId.in_(categoryIds)).all()
                    else:
                        services = []
                    serviceIds = [service.id for service in services]
                    if serviceIds:
                        professionals = Professionals.get_all_professionals().filter(Professionals.id.in_(serviceIds)).all()
                    else:
                        professionals = []

                    professionalIds = [professional.id for professional in professionals]
                    if professionalIds:
                        serviceRequests = ServiceHistory.get_active_serviceHistory().filter(ServiceHistory.professionalId.in_(professionalIds)).all()
                    else:
                        serviceRequests = []
                    return render_template('searchResults.html',user = user, searchOption=searchOption, searchText = searchText,categories = categories, services = services, professionals = professionals, serviceRequests = serviceRequests)
                
                if searchOption == 'Services':
                    services = Services.get_active_services().filter(Services.name.ilike(f'%{searchText}%')).all()
                    serviceIds = [service.id for service in services]
                    if serviceIds:
                        professionals = Professionals.get_all_professionals().filter(Professionals.id.in_(serviceIds)).all()
                    else:
                        professionals = []

                    professionalIds = [professional.id for professional in professionals]
                    if professionalIds:
                        serviceRequests = ServiceHistory.get_active_serviceHistory().filter(ServiceHistory.professionalId.in_(professionalIds)).all()
                    else:
                        serviceRequests = []
                    return render_template('searchResults.html',user = user,  searchOption=searchOption, searchText = searchText, services = services, professionals = professionals, serviceRequests = serviceRequests)
                
                if searchOption == 'Professionals':
                    professionals = Professionals.get_all_professionals().filter(or_(Professionals.fname.ilike(f'%{searchText}%'), Professionals.lname.ilike(f'%{searchText}%'))).all()
                    professionalIds = [professional.id for professional in professionals]
                    if professionalIds:
                        serviceRequests = ServiceHistory.get_active_serviceHistory().filter(ServiceHistory.professionalId.in_(professionalIds)).all()
                    else:
                        serviceRequests = []
                    return render_template('searchResults.html',user = user,  searchOption=searchOption, searchText = searchText, professionals = professionals, serviceRequests = serviceRequests)
                
                if searchOption == 'Customers':
                    customers = Customers.get_all_customers().filter(or_(Customers.fname.ilike(f'%{searchText}%'), Customers.lname.ilike(f'%{searchText}%'))).all()
                    customerIds = [customer.id for customer in customers]
                    if customerIds:
                        serviceRequests = ServiceHistory.get_active_serviceHistory().filter(ServiceHistory.customerId.in_(customerIds)).all()
                    else:
                        serviceRequests = []
                    return render_template('searchResults.html',user = user, searchOption=searchOption, searchText = searchText, customers = customers, serviceRequests = serviceRequests)
                
            if user.role == 'professional':
                if searchOption == 'location':
                    customers = Customers.get_all_customers().filter(Customers.address.ilike(f'%{searchText}%')).all()
                    customerIds = [customer.id for customer in customers]
                    serviceRequests = None
                    if customerIds:
                        serviceRequests = ServiceHistory.get_active_serviceHistory().filter(ServiceHistory.customerId.in_(customerIds))
                    serviceHistories = []
                    activeServiceRequests = []
                    newServiceRequests = []
                    if serviceRequests:
                        serviceHistories = serviceRequests.filter(ServiceHistory.professionalId == user.professionalDetails.id).all()
                        activeServiceRequests = serviceRequests.filter(ServiceHistory.status.in_([1, 2]), ServiceHistory.professionalId == user.professionalDetails.id).all()
                        newServiceRequests = serviceRequests.filter(and_(ServiceHistory.status == 0, ServiceHistory.is_requested == False), 
                                                                    and_(ServiceHistory.status == 0, ServiceHistory.is_requested == True, 
                                                                         ServiceHistory.professionalId == user.professionalDetails.id),  
                                                                         ServiceHistory.servicesId == user.professionalDetails.serviceId ).all()
                    return render_template('searchResults.html',user = user, searchOption=searchOption, searchText = searchText, newServiceRequests = newServiceRequests, activeServiceRequests = activeServiceRequests, serviceHistories = serviceHistories)
                if searchOption == 'pinCode':
                    customers = Customers.get_all_customers().filter(Customers.pinCode == searchText).all()
                    customerIds = [customer.id for customer in customers]
                    serviceRequests = None
                    if customerIds:
                        serviceRequests = ServiceHistory.get_active_serviceHistory().filter(ServiceHistory.customerId.in_(customerIds))
                    serviceHistories = []
                    activeServiceRequests = []
                    newServiceRequests = []
                    if serviceRequests:
                        serviceHistories = serviceRequests.filter(ServiceHistory.professionalId == user.professionalDetails.id).all()
                        activeServiceRequests = serviceRequests.filter(ServiceHistory.status.in_([1, 2]), ServiceHistory.professionalId == user.professionalDetails.id).all()
                        newServiceRequests = serviceRequests.filter(and_(ServiceHistory.status == 0, ServiceHistory.is_requested == False), 
                                                                    and_(ServiceHistory.status == 0, ServiceHistory.is_requested == True, 
                                                                         ServiceHistory.professionalId == user.professionalDetails.id),  
                                                                         ServiceHistory.servicesId == user.professionalDetails.serviceId  ).all()
                    return render_template('searchResults.html',user = user, searchOption=searchOption, searchText = searchText, newServiceRequests = newServiceRequests, activeServiceRequests = activeServiceRequests, serviceHistories = serviceHistories)
                
            if user.role == 'client':
                if searchOption == 'Categories':
                    categories = Categories.get_active_categories().filter(Categories.name.ilike(f'%{searchText}%')).all()
                    categoryIds = [category.id for category in categories]
                    if categoryIds:
                        services = Services.get_active_services().filter(Services.categoryId.in_(categoryIds)).all()
                    else:
                        services = []
                    serviceIds = [service.id for service in services]
                    if serviceIds:
                        serviceRequests = ServiceHistory.get_active_serviceHistory().filter(ServiceHistory.servicesId.in_(serviceIds), ServiceHistory.customerId == user.customerDetails.id)
                        serviceHistories = serviceRequests.all()
                    else:
                        serviceHistories = []
                    return render_template('searchResults.html',user = user, searchOption=searchOption, searchText = searchText, categories = categories, serviceHistories=serviceHistories)
                if searchOption == 'Services':
                    services = Services.get_active_services().filter(Services.name.ilike(f'%{searchText}%')).all()
                    serviceIds = [service.id for service in services]
                    if serviceIds:
                        serviceRequests = ServiceHistory.get_active_serviceHistory().filter(ServiceHistory.servicesId.in_(serviceIds), ServiceHistory.customerId == user.customerDetails.id)
                        serviceHistories = serviceRequests.all()
                    else:
                        serviceHistories = []
                    return render_template('searchResults.html',user = user, searchOption=searchOption, searchText = searchText, services = services, serviceHistories = serviceHistories)
                if searchOption == 'Professionals':
                    professionalQuery = Professionals.get_all_professionals().filter(or_(Professionals.fname.ilike(f'%{searchText}%'), Professionals.lname.ilike(f'%{searchText}%')))
                    professionals = professionalQuery.filter_by(is_approved = True, is_blocked = False, is_rejected = False, is_serviceAvailable = True).all()
                    existedProfessionals = professionalQuery.all()
                    professionalIds = [professional.id for professional in existedProfessionals]
                    if professionalIds:
                        serviceHistories = ServiceHistory.get_active_serviceHistory().filter(ServiceHistory.professionalId.in_(professionalIds), ServiceHistory.customerId == user.customerDetails.id).all()
                    else:
                        serviceHistories = []
                    return render_template('searchResults.html',user = user, searchOption = searchOption, searchText = searchText, professionals = professionals, serviceHistories = serviceHistories)
                if searchOption == 'location':
                    professionalQuery = Professionals.get_all_professionals().filter(Professionals.address.ilike(f'%{searchText}%'))
                    professionals = professionalQuery.filter_by(is_approved = True, is_blocked = False, is_rejected = False, is_serviceAvailable = True).all()
                    return render_template('searchResults.html',user = user, searchOption=searchOption, searchText = searchText,professionals = professionals)
                if searchOption == 'pinCode':
                    professionalQuery = Professionals.get_all_professionals().filter(Professionals.pinCode == searchText)
                    professionals = professionalQuery.filter_by(is_approved = True, is_blocked = False, is_rejected = False, is_serviceAvailable = True).all()
                    return render_template('searchResults.html',user = user, searchOption=searchOption, searchText = searchText, professionals = professionals)
                
            return render_template('searchResults.html',user = user)
    except Exception as e:
        db.session.rollback()
        print('Error: ' + str(e))
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))

# Admin routes and controllers

# Category Routes and controllers
@app.route('/new_category', methods= ['POST'])
@login_required
def addNewCategory():
    try:
        name = request.form.get('categoryName')

        check_category = Categories.query.filter(Categories.name.ilike(f'%{name}%'), Categories.is_deleted == False).first()
        if check_category:
            flash(('Category with same name exists.Give another name','danger'))
            return redirect(url_for('dashboard'))
        
        if not name:
            flash(('Please enter name field for category','danger'))
            return redirect(url_for('dashboard'))

        category = Categories(name = name)
        db.session.add(category)
        db.session.commit()
        flash((f" '{name}' category has succefully added", "success"))
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    
@app.route('/edit_category', methods= ['POST'])
@login_required
def editCategory():
    try:
        id = request.form.get('categoryId')
        name = request.form.get('categoryName')

        check_category = Categories.query.filter(Categories.name.ilike(f'%{name}%'), Categories.id != id, Categories.is_deleted == False ).first()
        if check_category:
            flash(('Category with same name exists.Give another name','danger'))
            return redirect(url_for('dashboard'))
        if not name:
            flash(('Please enter name field for category','danger'))
            return redirect(url_for('dashboard'))
        
        category = Categories.query.get(id)
        category.name = name
        db.session.commit()
        flash((f"'{name}' category has succefully edited", "success"))
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))

@app.route('/delete_category/<int:categoryId>')
@login_required
def deleteCategory(categoryId):
    try:
        category = Categories.query.get(categoryId)
        category.soft_delete()
        db.session.commit() 
        flash((f"'{category.name}'(and related services and professionals) has succefully deleted", "success"))
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    
# Service Routes and controllers
@app.route('/new_service', methods= ['POST'])
@login_required
def addNewService():
    try:
        name = request.form.get('serviceName')
        categoryId = request.form.get('categoryId')
        description = request.form.get('description')
        basePrice = request.form.get('basePrice')

        check_service = Services.query.filter(Services.name.ilike(f'%{name}%'), Services.is_deleted == False).first()
        if check_service:
            flash(('Service with same name exists.Give another name','danger'))
            return redirect(url_for('dashboard'))
        if any(not field for field in [name,categoryId,description,basePrice]):
                flash(('Please enter all fields for service','danger'))
                return redirect(url_for('dashboard'))


        category = Categories.query.get(categoryId)
        service = Services(name = name,
                           description = description,
                           basePrice = basePrice,
                           category= category)
        db.session.add(service)
        db.session.commit()
        flash((f"'{name}' service has succefully added", "success"))
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    
@app.route('/edit_service', methods= ['POST'])
@login_required
def editService():
    try:
        serviceId = request.form.get('serviceId',None)
        name = request.form.get('serviceName', None)
        categoryId = request.form.get('categoryId', None)
        description = request.form.get('description', None)
        basePrice = request.form.get('basePrice', None)

        check_service = Services.query.filter(Services.name.ilike(f'%{name}%'), Services.id != serviceId, Services.is_deleted == False).first()
        if check_service:
            flash(('Service with same name exists.Give another name','danger'))
            return redirect(url_for('dashboard'))
        if any(not field for field in [name,categoryId,description,basePrice]):
                flash(('Please enter all fields for editing service','danger'))
                return redirect(url_for('dashboard'))

        service = Services.query.get(serviceId)
        category = Categories.query.get(categoryId)

        if name:
            service.name = name
        if service.description:
            service.description = description
        if service.basePrice: 
            service.basePrice = basePrice
        if service.category:
            service.category= category
        db.session.commit()
        flash((f"'{name}' service has succefully edited", "success"))
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    

@app.route('/delete_service/<int:serviceId>')
@login_required
def deleteService(serviceId):
    try:
        service = Services.query.get(serviceId)
        service.soft_delete()
        db.session.commit() 
        flash((f"'{service.name}'(and the related professionals) has succefully deleted ", "success"))
        return redirect(url_for('dashboard'))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    

# Client routes and controllers

# view all service under a category
@app.route('/services/<int:categoryId>')
@login_required
@active_account
def viewServices(categoryId):
    user = Users.query.get(current_user.id)
    services = Services.get_active_services_byId(categoryId).all()
    return render_template('services.html', user=user, services = services)

    
# Professional Routes and controllers

@app.route('/updateApprove/<int:professionalId>')
@login_required
@active_account
def updateProfessionalApproved(professionalId):
    try:
        professional = Professionals.query.get(professionalId)
        professional.updateApprove()
        db.session.commit()
        flash((f"{professional.fname}'s account successfully Approved!","success"))
        return redirect(url_for(dashboard))
    
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard')) 
    
@app.route('/updateReject/<int:professionalId>')
@login_required
@active_account
def updateProfessionalReject(professionalId):
    try:
        professional = Professionals.query.get(professionalId)
        professional.updateReject()
        db.session.commit()
        flash((f"{professional.fname}'s account successfully Rejected!","warning"))
        return redirect(url_for(dashboard))
    
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard')) 

@app.route('/update_professional_block/<int:professionalId>')
@login_required   
@active_account
def updateProfessionalBlock(professionalId):
    try:
        professional = Professionals.query.get(professionalId)
        professional.updateBlock()
        db.session.commit()
        if professional.is_blocked:
            flash((f"{professional.fname}'s account successfully bloked.","warning"))
        else:
            flash((f"{professional.fname}'s account successfully unbloked.","success"))
        return redirect(url_for(dashboard))
    
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard')) 

@app.route('/delete_professional/<int:professionalId>')
@login_required 
def deleteProfessional(professionalId):
    try:
        professional = Professionals.query.get(professionalId)
        professional.soft_delete()
        db.session.commit()
        flash((f"{professional.fname}'s account successfully deleted!","warning"))
        return redirect(url_for(dashboard))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    
# Customer routes for delete and block

@app.route('/update_customer_block/<int:customerId>')
@login_required   
def updateCustomerBlock(customerId):
    try:
        customer = Customers.query.get(customerId)
        customer.updateBlock()
        db.session.commit()
        if customer.is_blocked:
            flash((f"{customer.fname}'s account successfully bloked.","warning"))
        else:
            flash((f"{customer.fname}'s account successfully unbloked.","success"))
        return redirect(url_for(dashboard))
    
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard')) 

@app.route('/delete_customer/<int:customerId>')
@login_required 
def deleteCustomer(customerId):
    try:
        customer = Customers.query.get(customerId)
        customer.soft_delete()
        db.session.commit()
        flash((f"{customer.fname}'s account successfully deleted!","warning"))
        return redirect(url_for(dashboard))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    
    


# Book a  new service
@app.route('/booking/<int:serviceId>')
@login_required
@active_account
def bookService(serviceId):
    try:
        service = Services.query.get(serviceId)
        user = Users.query.get(current_user.id)
        serviceHistory = ServiceHistory(service = service, customer = user.customerDetails)
        db.session.add(serviceHistory)
        db.session.commit()
        flash(("Booking successfully created!","success"))
        return redirect(url_for(dashboard))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    
@app.route('/request_service/<int:professionalId>')
@login_required
@active_account
def requestService(professionalId):
    try:
        user = Users.query.get(current_user.id)
        professional = Professionals.query.get(professionalId)
        service = professional.service
        serviceHistory = ServiceHistory(is_requested = True ,service = service, customer = user.customerDetails, professional = professional)
        db.session.add(serviceHistory)
        db.session.commit()
        flash(("Request successfully created!","success"))
        return redirect(url_for(dashboard))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    
# Accept a service request made by Custemer/ Client
@app.route('/accept_servicerequest/<int:serviceRequestId>')
@login_required 
@active_account
def acceptServiceRequest(serviceRequestId):
    try:
        serviceRequest = ServiceHistory.query.get(serviceRequestId)
        user = Users.query.get(current_user.id)
        serviceRequest.dateAccepted = datetime.now()
        serviceRequest.status = 1
        serviceRequest.professional = user.professionalDetails
        db.session.commit()
        flash(("Service request have successfully accepted","success"))
        return redirect(url_for(dashboard))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    
# reject a direct service request from customer by professional
@app.route('/reject_servicerequest/<int:serviceRequestId>')
@login_required 
@active_account
def rejectServiceRequest(serviceRequestId):
    try:
        serviceRequest = ServiceHistory.query.get(serviceRequestId)
        user = Users.query.get(current_user.id)
        if user.role != 'professional':
            flash(("A service request can reject by a professional only.","danger"))
            return redirect(url_for(dashboard))
        if not serviceRequest.is_requested:
            flash(("Service request cannot reject if it in not requested by customer","danger"))
            return redirect(url_for(dashboard))
        serviceRequest.status = 4
        db.session.commit()
        flash(("Service request have successfully rejected","warning"))
        return redirect(url_for(dashboard))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    
@app.route('/complete_servicerequest/<int:serviceRequestId>')
@login_required 
@active_account
def completeServiceRequest(serviceRequestId):
    try:
        serviceRequest = ServiceHistory.query.get(serviceRequestId)
        user = Users.query.get(current_user.id)
        if user.role != 'professional':
            flash(("A service request can Complete by a professional only.","danger"))
            return redirect(url_for(dashboard))
        if serviceRequest.status != 1:
            flash(("Only approved service request can be mark as completed","danger"))
            return redirect(url_for(dashboard))
        if not serviceRequest.professionalId == user.professionalDetails.id:
            flash(("This service is not belong to your account","danger"))
            return redirect(url_for(dashboard))
        
        serviceRequest.dateCompleted = datetime.now()
        serviceRequest.status = 2
        db.session.commit()
        flash(("Service request have successfully completed","success"))
        return redirect(url_for(dashboard))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))

@app.route('/view_servicerequest/<int:serviceRequestId>')
@login_required 
@active_account
def viewServiceRequest(serviceRequestId):
    try:
        user = Users.query.get(current_user.id)
        serviceRequest = ServiceHistory.query.get(serviceRequestId)
        return render_template('viewServiceRequest.html',user=user, serviceRequest=serviceRequest)
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    
# delete  a request by customer..Only available if status is pending / 1
@app.route('/delete_servicerequest/<int:serviceRequestId>')
@login_required 
@active_account
def deleteServiceRequest(serviceRequestId):
    try:
        serviceRequest = ServiceHistory.query.get(serviceRequestId)
        user = Users.query.get(current_user.id)
        if serviceRequest.status != 0:
            flash(("Only pending service request can be deleted","danger"))
            return redirect(url_for(dashboard))
        if not serviceRequest.customerId == user.customerDetails.id:
            flash(("This service is not belong to your account","danger"))
            return redirect(url_for(dashboard))
        
        serviceRequest.status = 5
        serviceRequest.soft_delete()
        db.session.commit()
        flash(("Service request have successfully deleted","warning"))
        return redirect(url_for(dashboard))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    
# Close the service request after customer complete the service request
@app.route('/close_servicerequest/<int:serviceRequestId>')
@login_required 
@active_account
def closeServiceRequest(serviceRequestId):
    try:
        serviceRequest = ServiceHistory.query.get(serviceRequestId)
        user = Users.query.get(current_user.id)
        if serviceRequest.status != 2:
            flash(("Only Completed service request can be closed!!","danger"))
            return redirect(url_for(dashboard))
        if not serviceRequest.customerId == user.customerDetails.id:
            flash(("This service is not belong to your account","danger"))
            return redirect(url_for(dashboard))
        
        serviceRequest.status = 3
        db.session.commit()
        flash(("Service request have successfully closed","success"))
        return redirect(url_for('serviceReview',serviceRequestId = serviceRequest.id  ))
    except Exception as e:
        db.session.rollback()
        flash(("Error:"+str(e),'danger'))
        return redirect(url_for('dashboard'))
    

@app.route('/review_servicerequest/<int:serviceRequestId>', methods = ['GET', 'POST'])
@login_required 
@active_account
def serviceReview(serviceRequestId):
    user = Users.query.get(current_user.id)
    if request.method == 'GET':
        return render_template('reviewService.html', user = user, serviceRequestId =serviceRequestId)
    else:
        rating = request.form.get("rating")
        reviewText = request.form.get("remarks")
        if not rating or not reviewText:
            flash(("Please enter all fields","danger"))
            return redirect(url_for('serviceReview', serviceRequestId=serviceRequestId))
        
        serviceRequest = ServiceHistory.query.get(serviceRequestId)
        review = Reviews(rating = int(rating),
                         reviewText = reviewText,
                         serviceHistory = serviceRequest )
        db.session.add(review)
        db.session.commit()
        flash(("Review has successfully added","success"))
        return redirect(url_for('dashboard'))
    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/error')
def error():
    return render_template('error.html')


