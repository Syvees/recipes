from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


class Recipes: # MODEL AFTER RECIPES TABLE
    DB = "recipes"
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.cooked_date = data["cooked_date"]
        self.under_30_mins = data["under_30_mins"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.cook = None

    @classmethod # INSERT A RECIPE
    def save_recipe(cls, data):
        query = """INSERT INTO recipes (name, description, instructions, cooked_date, under_30_mins, user_id) 
        VALUES (%(name)s, %(description)s, %(instructions)s, %(cooked_date)s, %(under_30_mins)s, %(user_id)s)"""
        results = connectToMySQL(cls.DB).query_db(query, data)

    @classmethod # GET ALL RECIPES
    def get_all_recipes_with_users(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id ORDER BY recipes.id"
        results = connectToMySQL(cls.DB).query_db(query)
        recipes = []
        for row in results:
            this_recipe = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            this_recipe.cook = user.Users(user_data)
            recipes.append(this_recipe)
        return recipes
    
    @classmethod # GET ALL RECIPES BY RECIPE ID
    def get_all_recipes_with_users_by_id(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        for row in results:
            this_recipe = cls(row)
            user_data = {
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"]
            }
            this_recipe.cook = user.Users(user_data)
        return this_recipe
    
    @classmethod # UPDATE A RECIPE
    def update_recipe (cls,data):
        query = """UPDATE recipes
                SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, 
                cooked_date=%(cooked_date)s, under_30_mins=%(under_30_mins)s
                WHERE id = %(id)s"""
        result = connectToMySQL(cls.DB).query_db(query, data) 
        return result
    
    @classmethod # DELETE A RECIPE
    def delete_recipe (cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        result = connectToMySQL(cls.DB).query_db(query, data) 
        return result
    
    @staticmethod # NEW RECIPE VALIDATIONS
    def validate_add_recipe(data): 
        is_valid = True
        if len(data["name"]) < 3:
            flash("Please add a recipe name.", "add_recipe")
            is_valid = False
        if len(data["description"]) < 3:
            flash("Please add a description.", "add_recipe")
            is_valid = False
        if len(data["instructions"]) < 3:
            flash("Please add instructions.", "add_recipe")
            is_valid = False
        if data["cooked_date"] == "":
            flash("Please select a date.", "add_recipe")
            is_valid = False
        if "under_30_mins" not in data: 
            flash("Please select a cook time.", "add_recipe")
            is_valid = False
        return is_valid