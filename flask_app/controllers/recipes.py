from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.recipe import Recipes
from flask_bcrypt import Bcrypt 
from flask import flash

@app.route("/recipes") # GO TO DASHBOARD
def display_dashboard():
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    all_recipes = Recipes.get_all_recipes_with_users()
    return render_template("dashboard.html", recipes=all_recipes)

@app.route("/recipes/<int:recipe_id>") # VIEW EACH RECIPE
def display_recipe(recipe_id):
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    data = {
        'id':recipe_id  
    }
    show_recipe = Recipes.get_all_recipes_with_users_by_id(data)
    return render_template("recipe.html", one_recipe=show_recipe)

@app.route("/recipes/edit/<int:recipe_id>") # RENDER EDIT RECIPE PRE-POPULATED
def edit_recipe(recipe_id):
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    data = {
        'id':recipe_id  
    }
    one_recipe = Recipes.get_all_recipes_with_users_by_id(data)
    print(one_recipe.name)
    print(one_recipe.under_30_mins)

    return render_template("edit.html", one_recipe=one_recipe)

@app.route("/recipes/update/<int:recipe_id>", methods=["POST"]) # UPDATE THE RECIPE AND POST
def update_recipe(recipe_id):
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    id = recipe_id
    if not Recipes.validate_add_recipe(request.form): # VALIDATION AND RETURN TO INDEX
        return redirect(f"/recipes/edit/{id}")
    data = {
            "id" : recipe_id,
            "name" : request.form["name"],
            "description" : request.form["description"],
            "instructions" : request.form["instructions"],
            "cooked_date" : request.form["cooked_date"],
            "under_30_mins" : request.form["under_30_mins"],
            "user_id" : session["logged_in_id"]
        }
    Recipes.update_recipe(data)
    return redirect("/recipes")

@app.route("/recipes/new") # RENDER BLANK RECIPE FORM
def display_recipe_form():
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    return render_template("new.html")

@app.route("/recipes/add", methods=["POST"]) # ADD RECIPE AND POST
def add_recipe():
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    if not Recipes.validate_add_recipe(request.form): # VALIDATION AND RETURN TO INDEX
        return redirect("/recipes/new")
    data = {
            "name" : request.form["name"],
            "description" : request.form["description"],
            "instructions" : request.form["instructions"],
            "cooked_date" : request.form["cooked_date"],
            "under_30_mins" : request.form["under_30_mins"],
            "user_id" : session["logged_in_id"]
        }
    Recipes.save_recipe(data)
    return redirect("/recipes")

@app.route("/recipes/delete/<int:recipe_id>") # DELETE A RECIPE
def delete_recipe(recipe_id):
    if "logged_in_id" not in session: # CHECK IF IN SESSION
        return redirect ("/")
    data = {
        'id':recipe_id  
    }
    Recipes.delete_recipe(data)
    return redirect("/recipes")

