from applications.models import *

def addAdminDetails():
    try:
        checkUser = Users.query.filter_by(role = "admin").first()
        if not checkUser:
            fname = "Nick"
            lname = "Fury"
            username = "admin"
            email = "admin@gmail.com"
            password = "admin"
            role = "admin"
            admin = Admin(fname = fname, lname = lname)
            user = Users(username = username,
                        email = email,
                        password = password,
                        role = role,
                        adminDetails = admin)

            db.session.add(user)
            db.session.commit()
    except Exception as e:
        print(f"Exception in addAdminDetails(): {type(e).__name__}: {str(e)}")