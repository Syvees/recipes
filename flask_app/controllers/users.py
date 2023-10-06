from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user import Users
from flask_bcrypt import Bcrypt 
from flask import flash

bcrypt = Bcrypt(app) # we are creating an object called bcrypt which is made by invoking the function Bcrypt with our app as an argument

@app.route("/") # RENDER REGISTER AND LOGIN FORM
def display_form ():
    return render_template("index.html")

@app.route("/add", methods=["POST"]) #  ADD A USER AND POST
def add_user():
    if not Users.validate_user(request.form): # VALIDATION AND REDIRECT TO INDEX
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password']) # HASHING PASSWORD
    data = {
        "first_name":request.form["first_name"],
        "last_name":request.form["last_name"],
        "email":request.form["email"],
        "password":pw_hash
    }  
    user_id=Users.save(data)
    session["logged_in_id"]=user_id # USER ID SAVE IN SESSION
    session["logged_in_first_name"]=request.form["first_name"] # USER NAME SAVE IN SESSION
    return redirect("/recipes")

@app.route("/login", methods=["POST"]) # CHECK LOGIN CREDENTIALS
def validate_login():
    if not Users.validate_login(request.form): # CHECK IF USER EXISTS IN DB
        return redirect("/")
    return redirect("/recipes")

@app.route("/logout") # LOGOUT
def logout():
    session.clear()
    return redirect("/")