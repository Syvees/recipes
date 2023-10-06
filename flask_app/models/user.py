from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt 
from flask import flash

bcrypt = Bcrypt(app) # we are creating an object called bcrypt which is made by invoking the function Bcrypt with our app as an argument

class Users: # MODEL AFTER USERS TABLE
    DB = "recipes"
    def __init__ (self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod # INSERT A USER
    def save(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password) 
                VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s )"""
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod # GET USER BY EMAIL
    def get_one_by_email(cls,data):
        query = """SELECT * FROM users 
                WHERE email = %(email)s"""  
        result = connectToMySQL(cls.DB).query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod # NEW USER VALIDATIONS
    def validate_user(data): 
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True
        if len(data["first_name"]) < 2:
            flash("First Name must be at least 2 characters.", "register")
            is_valid = False
        if not data["first_name"].isalpha() and data["first_name"]!= "":
            flash("First Name should be letters only.", "register")
            is_valid = False
        if len(data["last_name"]) < 2:
            flash("Last Name must be at least 2 characters.", "register")
            is_valid = False
        if not data["last_name"].isalpha() and data["last_name"]!= "":
            flash("Last Name should be letters only.", "register")
            is_valid = False
        if Users.get_one_by_email({"email":data["email"]}): # CHECK IF USER ALREADY EXISTS
            flash("User already exists.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]): # CHECK IF EMAIL IS VALID
            flash("Invalid email format.", "register")
            is_valid = False
        if len(data["password"]) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if data["password"] != data["confirm_password"]:
            flash("Password does not match.", "register")
            is_valid = False
        return is_valid

    @staticmethod # LOGIN VALIDATIONS
    def validate_login(data): 
        one_user = Users.get_one_by_email(data)
        if one_user:
            if bcrypt.check_password_hash(one_user.password, data["password"]): # CHECK HASHED PASSWORD IF MATCH
                session["logged_in_first_name"]=one_user.first_name # SAVE IN SESSION
                session["logged_in_id"]=one_user.id
                return True
        flash("Email or Password is incorrect.", "login")
        return False