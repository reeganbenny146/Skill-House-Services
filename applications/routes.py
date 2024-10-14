from main import app
from flask import render_template, session, url_for, redirect, request ,flash
from applications.models import *


@app.route('/', methods=["GET","POST"])
def login():
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
        if not user:
            flash(('Please enter a valid email..!!!','danger'))
            return redirect(url_for('login'))
        else:
            if user.password == password:
                session['email'] = user.email
                session['role'] = user.role
                flash((user.email + 'have succesfully logged in!!', 'success'))
                return redirect(url_for('home'))
            else:
                flash(('invalid password..!!!','danger'))
                return redirect(url_for('login'))


@app.route('/role', methods=["GET", "POST"])
def role():
    if request.method == 'GET':
        return render_template('role.html')
    else:
        role = request.form.get("userType",None)
        if role:
            return render_template('registration.html', user_role = role)
        else:
            flash(('Please select a role.','danger'))
            return redirect(url_for('role'))

@app.route('/registration',methods = ['GET', 'POST'])
def registration():
    if request.method == 'GET': 
        return render_template('registration.html')
    else:
        fname = request.form.get('firstName')
        lname = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        address = request.form.get('address')
        mob = request.form.get('mobileNumber')
        pin = request.form.get('pin')

        if any(not field for field in [fname, lname, email, password, cpassword, address, mob, pin]):
            flash(('Please enter all field','danger'))
            return redirect(url_for('registration'))

@app.route('/home')
def home():
    return render_template('home.html')