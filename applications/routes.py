from main import app
from flask import render_template, session, url_for, redirect, request ,flash
from applications.models import *


# User login routes
@app.route('/login', methods=["GET","POST"])
def login():

    if 'email' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == "GET":
        return render_template('login.html')
    else:
        email = request.form.get('email',None)
        password = request.form.get('password', None)
        print(email)
        if not email  or not password :
            flash(('Email and password must not empty..!!!','danger'))
            return redirect(url_for('login'))
        user = Users.query.filter_by(email = email).first()
        print(vars(user))
        if not user:
            flash(('Please enter a valid email..!!!','danger'))
            return redirect(url_for('login'))
        else:
            if user.password == password:
                # session['']
                session['email'] = user.email
                session['role'] = user.role
                flash((user.email + 'have succesfully logged in!!', 'success'))
                return redirect(url_for('dashboard'))
            else:
                flash(('invalid password..!!!','danger'))
                return redirect(url_for('login'))

# User role select
@app.route('/role',methods = ["GET","POST"])
def role():
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
        if not session or not session['reg_user_role']:
            flash(('Please select a role.','danger'))
            return redirect(url_for('role'))
        elif session['reg_user_role'] == 'professional':
            if 'services' not in session or not session['services']:
                servicesList = Services.query.all()
        if request.method == "GET":
            return render_template('registration.html')
        else:
            fname = request.form.get('firstName')
            lname = request.form.get('lastName')
            image = request.files.get('profileImage',None)
            email = request.form.get('email')
            password = request.form.get('password')
            cpassword = request.form.get('cpassword')
            address = request.form.get('address')
            mob = request.form.get('mobileNumber')
            pin = request.form.get('pincode')
            role = session['reg_user_role']
            if any(not field for field in [fname, lname, email, password, cpassword, address, mob, pin, role]):
                flash(('Please enter all field','danger'))
                return redirect(url_for('registration'))

            imageFilePath = None
            profilePhotoPath = ''
            if image:
                # import libraries for changing filename
                import os
                import re

                # Sanitize emial to have a unique file name(for image or resume)
                sanitized_email = re.sub(r'[^a-zA-Z0-9]', '_', email)

                file_ext = os.path.splitext(image.filename)[1]
                new_filename = f"{sanitized_email}{file_ext}"
                print("hi")
                if image:
                    imageFilePath = 'images\\users\\' + new_filename
                    print(imageFilePath)
                    profilePhotoPath = os.path.join('static', imageFilePath)
                    os.makedirs(os.path.dirname(profilePhotoPath), exist_ok=True)
                    print("absolute_path ="+profilePhotoPath)
                    image.save(profilePhotoPath)          

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
                incentive = request.form.get('incentive')
                resume = request.files.get('resume')
                professional = Professionals(fname= fname,
                                                lname = lname,
                                                experience = experience,
                                                resumePath= "",
                                                profilePhotoPath = profilePhotoPath,
                                                mobileNo = mob,
                                                address = address,
                                                pinCode = int(pin),
                                                serviceId = serviceId,
                                                incentive = incentive
                                                )
                user = Users(email = email,
                            password = password,
                            role = session['reg_user_role'],
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
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    
    return render_template('/dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/error')
def error():
    return render_template('/error.html')
