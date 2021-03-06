import os
from flask import Flask, render_template, redirect, request, url_for, session
from flask import flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
import re
import uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.storage.blob import __version__
from azure.core.exceptions import ResourceExistsError
from werkzeug.utils import secure_filename
import time
from datetime import datetime

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["IMAGE_UPLOADS"] = "./upload_images"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]

mongo = PyMongo(app)


# Handling error and displaying error.html page
# Credit: https://www.askpython.com/python-modules/flask/flask-error-handling
@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html'), 500


@app.errorhandler(404)
def internal_error(error):
    return render_template('error.html'), 404


# Start app on index.html
@app.route('/')
def index():

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    return render_template('index.html',
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find(),
                           results_winename="",
                           results_vintage="",
                           results_colour="",
                           results_country="",
                           results_region="",
                           results_grape="",
                           # Credit: https://docs.mongodb.com/manual/reference/operator/aggregation/sample/
                           # Credit: https://stackoverflow.com/questions/25436630/mongodb-how-to-find-and-then-aggregate
                           carousel_one=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url": {"$ne": ""}}},
                                        {"$sample": {"size": 1}}]),
                           carousel_two=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url": {"$ne": ""}}},
                                        {"$sample": {"size": 1}}]),
                           carousel_three=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url": {"$ne": ""}}},
                                        {"$sample": {"size": 1}}])
                           )


# Log In/Out and Register routes
@app.route('/login_page')
def login_page():

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    return render_template('login.html',
                           user_name=user_return)


# Credit: https://edubanq.com/programming/mongodb/creating-a-user-login-system-using-python-flask-and-mongodb/
@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'),
                         login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('my_profile_page'))

    return render_template("login.html",
                           password_error='Invalid username/password combination')


# Credit: https://pythonbasics.org/flask-sessions/
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


# Credit: https://edubanq.com/programming/mongodb/creating-a-user-login-system-using-python-flask-and-mongodb/
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        SpecialSym = ['$', '@', '#', '%', '!']

        userVal = request.form['username']

        if re.match("^[a-zA-Z0-9*]+$", userVal) and not userVal.isnumeric():
            # Credit: https://stackoverflow.com/questions/15580917/python-data-validation-using-regular-expression
            passVal = request.form['pass']
            # Credit: https://www.geeksforgeeks.org/password-validation-in-python/#:~:text=Conditions%20for%20a%20valid%20password%20are%3A%201%20Should,be%20between%206%20to%2020%20characters%20long.%20
            if len(passVal) < 6:
                return render_template("register.html", register_error='password should be at least 6 characters')
            if len(passVal) > 10:
                return render_template("register.html", register_error='password should be no more than 10 characters')
            if not any(char.isdigit() for char in passVal):
                return render_template("register.html", register_error='password should have at least one numeral')
            if not any(char.isupper() for char in passVal):
                return render_template("register.html", register_error='password should have at least one uppercase letter')
            if not any(char.islower() for char in passVal):
                return render_template("register.html", register_error='password should have at least one lowercase letter')
            if not any(char in SpecialSym for char in passVal):
                return render_template("register.html", register_error='password should have at least one of the symbols $, @, #, % or !')
            else:
                if existing_user is None:
                    hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
                    users.insert({'name': request.form['username'], 'password': hashpass})
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                return render_template("register.html", register_error='That username already exists')
        else:
            return render_template("register.html", register_error='Please enter a valid username of text and numbers, with no spaces')

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    return render_template('register.html',
                           user_name=user_return)

    return ''


# Add/Delete Wine routes
@app.route('/add_wine_page')
def add_wine_page():

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    return render_template("add_wine.html",
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find()
                           )


# Refresh Add Wine Form route
@app.route('/populate_form')
def populate_form():

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    return render_template("add_wine.html",
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find()
                           )


@app.route('/add_wine', methods=["GET", "POST"])
def add_wine():

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    nameadd = request.values.get("name")
    vintageadd = request.values.get("vintage")
    colouradd = request.values.get("colour")
    countryadd = request.values.get("country")
    regionadd = request.values.get("region")
    grapeadd = request.values.get("grape")
    if not any(char.islower() for char in nameadd):
        flash('wine name must be populated')
        return render_template("add_wine.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               results_vintage=vintageadd,
                               results_colour=colouradd,
                               results_country=countryadd,
                               results_region=regionadd,
                               results_grape=grapeadd
                               )

    if not all(char.isdigit() for char in vintageadd):
        flash('vintage must be 4 numerals')
        return render_template("add_wine.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               results_name=nameadd,
                               results_colour=colouradd,
                               results_country=countryadd,
                               results_region=regionadd,
                               results_grape=grapeadd
                               )

    currentYear = datetime.now().year
    if int(vintageadd) > currentYear:
        flash('you have entered a vintage that is in the future!')
        return render_template("add_wine.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               results_name=nameadd,
                               results_colour=colouradd,
                               results_country=countryadd,
                               results_region=regionadd,
                               results_grape=grapeadd
                               )

    if nameadd == "" or vintageadd == "" or colouradd == "" or countryadd == "" or regionadd == "" or grapeadd == "":
        flash('all fields must be populated')
        return render_template("add_wine.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               results_name=nameadd,
                               results_vintage=vintageadd,
                               results_colour=colouradd,
                               results_country=countryadd,
                               results_region=regionadd,
                               results_grape=grapeadd
                               )

    wines = mongo.db.wines
    existing_wine = wines.find_one({"wine_name": nameadd.title(),
                                    "vintage": vintageadd,
                                    "colour": colouradd,
                                    "country": countryadd,
                                    "region": regionadd,
                                    "grape": grapeadd,
                                    "photo_url": "",
                                    "tasting_notes": ""})
    if existing_wine is not None:
        flash("That wine has already been added")
        return render_template("add_wine.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               results_name="",
                               results_vintage="",
                               results_colour="",
                               results_country="",
                               results_region="",
                               results_grape=""
                               )

    # Credit: https://pythonprogramming.net/flash-flask-tutorial/
    flash("The wine has been added")
    return render_template("add_wine.html",
                           user_name=user_return,
                           insert=mongo.db.wines.insert_one({"wine_name": nameadd.title(),
                                                             "vintage": vintageadd,
                                                             "colour": colouradd,
                                                             "country": countryadd,
                                                             "region": regionadd,
                                                             "grape": grapeadd,
                                                             "photo_url": "",
                                                             "tasting_notes": "",
                                                             "added_by": session['username']}),
                           results_winename="",
                           results_vintage="",
                           results_colour="",
                           results_country="",
                           results_region="",
                           results_grape="",
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find(),
                           results=mongo.db.wines.find({"wine_name": nameadd.title(),
                                                        "vintage": vintageadd,
                                                        "colour": colouradd,
                                                        "country": countryadd,
                                                        "region": regionadd,
                                                        "grape": grapeadd,
                                                        "photo_url": "",
                                                        "tasting_notes": ""})
                           )


@app.route('/delete_wine_page/<wine_id>')
def delete_wine_page(wine_id):

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    return render_template("delete_wine_page.html",
                           user_name=user_return,
                           wine_id=wine_id)


@app.route('/delete_wine/<wine_id>')
def delete_wine(wine_id):
    # Credit: https://pythonprogramming.net/flash-flask-tutorial/
    flash("The wine has been deleted")

    if 'username' in session:
        user_return = 'User: ' + session['username']
        added_by = session['username']
    else:
        user_return = 'Cave du Vins'

    if session['username'] == 'admin':
        return render_template("my_profile.html",
                               delete=mongo.db.wines.remove({'_id': ObjectId(wine_id)}),
                               user_name=user_return,
                               added_by=added_by,
                               results=mongo.db.wines.find(),
                               notes=mongo.db.wines.find(
                                   {"$or": [
                                       {'tasting_notes': {'$regex': '.*' + added_by + '.*'}},
                                       {'tasting_notes': {'$regex': '.*' + added_by.title() + '.*'}}]}
                               ))

    return render_template("my_profile.html",
                           delete=mongo.db.wines.remove({'_id': ObjectId(wine_id)}),
                           user_name=user_return,
                           added_by=added_by,
                           results=mongo.db.wines.find({'added_by': added_by}),
                           notes=mongo.db.wines.find(
                               {"$or": [
                                   {'tasting_notes': {'$regex': '.*' + added_by + '.*'}},
                                   {'tasting_notes': {'$regex': '.*' + added_by.title() + '.*'}}]}
                                   ))


# Add/Deleted Documents to/from Collections routes
@app.route('/add_country', methods=["GET", "POST"])
def add_country():

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    countryadd = request.values.get("addcountry")
    existing_country = mongo.db.country.find_one({'country': countryadd})
    if not any(char.islower() for char in countryadd) and not any(char.isupper() for char in countryadd):
        flash('country must be populated')
        return render_template("add_wine.html",
                               user_name=user_return,
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find()
                               )

    # Credit: https://pythonprogramming.net/flash-flask-tutorial/
    flash(countryadd + " has been added")
    if existing_country is None:
        return render_template("add_wine.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               insert=mongo.db.country.insert_one(
                                    {"country": countryadd.title()}
                                    ))
    return render_template("add_wine.html",
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find()
                           )


@app.route('/add_region', methods=["GET", "POST"])
def add_region():

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    regionadd = request.values.get("addregion")
    existing_region = mongo.db.region.find_one({'region': regionadd})
    if not any(char.islower() for char in regionadd) and not any(char.isupper() for char in regionadd):
        flash('region must be populated')
        return render_template("add_wine.html",
                               user_name=user_return,
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find()
                               )

    # Credit: https://pythonprogramming.net/flash-flask-tutorial/
    flash(regionadd + " has been added")
    if existing_region is None:
        return render_template("add_wine.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               insert=mongo.db.region.insert_one(
                                    {"region": regionadd.title()}
                                    ))
    return render_template("add_wine.html",
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find()
                           )


@app.route('/add_grape', methods=["GET", "POST"])
def add_grape():

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    grapeadd = request.values.get("addgrape")
    existing_grape = mongo.db.grape.find_one({'grape': grapeadd})
    if not any(char.islower() for char in grapeadd) and not any(char.isupper() for char in grapeadd):
        flash('grape must be populated')
        return render_template("add_wine.html",
                               user_name=user_return,
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find())

    # Credit: https://pythonprogramming.net/flash-flask-tutorial/
    flash(grapeadd + " has been added")
    if existing_grape is None:
        return render_template("add_wine.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               insert=mongo.db.grape.insert_one(
                                    {"grape": grapeadd.title()}
                                    ))
    return render_template("add_wine.html",
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find()
                           )


@app.route('/delete_category_page/<category_id>')
def delete_category_page(category_id):

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    return render_template('categories.html',
                           category_id=category_id,
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find()
                           )


@app.route('/delete_category/<category_id>', methods=["GET", "POST"])
def delete_category(category_id):

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    category = request.values.get("category")

    # Credit: https://pythonprogramming.net/flash-flask-tutorial/
    if category_id == "country":
        if category == "select":
            flash("no " + category_id + " has been deleted")
            return render_template('add_wine.html',
                                   user_name=user_return,
                                   colours=mongo.db.colours.find(),
                                   country=mongo.db.country.find(),
                                   region=mongo.db.region.find(),
                                   grape=mongo.db.grape.find()
                                   )
        flash(category + " has been deleted")
        return render_template('add_wine.html',
                               user_name=user_return,
                               category_id="country",
                               delete=mongo.db.country.delete_one({'country': category}),
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find()
                               )
    if category_id == "region":
        if category == "select":
            flash("no " + category_id + " has been deleted")
            return render_template('add_wine.html',
                                   user_name=user_return,
                                   colours=mongo.db.colours.find(),
                                   country=mongo.db.country.find(),
                                   region=mongo.db.region.find(),
                                   grape=mongo.db.grape.find()
                                   )
        flash(category + " has been deleted")
        return render_template('add_wine.html',
                               user_name=user_return,
                               category_id="region",
                               delete=mongo.db.region.delete_one({'region': category}),
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find()
                               )
    if category_id == "grape":
        if category == "select":
            flash("no " + category_id + " has been deleted")
            return render_template('add_wine.html',
                                   user_name=user_return,
                                   colours=mongo.db.colours.find(),
                                   country=mongo.db.country.find(),
                                   region=mongo.db.region.find(),
                                   grape=mongo.db.grape.find()
                                   )
        flash(category + " has been deleted")
        return render_template('add_wine.html',
                               user_name=user_return,
                               category_id="grape",
                               delete=mongo.db.grape.delete_one({'grape': category}),
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find()
                               )


# Browse Wines routes
@app.route('/search_page')
def search_page():

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    return render_template('index.html',
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find(),
                           results_winename="",
                           results_vintage="",
                           results_colour="",
                           results_country="",
                           results_region="",
                           results_grape="",
                           # Credit: https://docs.mongodb.com/manual/reference/operator/aggregation/sample/
                           # Credit: https://stackoverflow.com/questions/25436630/mongodb-how-to-find-and-then-aggregate
                           carousel_one=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url":  {"$ne": ""}}},
                                        {"$sample": {"size": 1}}]),
                           carousel_two=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url": {"$ne": ""}}},
                                        {"$sample": {"size": 1}}]),
                           carousel_three=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url": {"$ne": ""}}},
                                        {"$sample": {"size": 1}}])
                           )


@app.route('/populate_search')
def populate_search():

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    return render_template("index.html",
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find(),
                           results_winename="",
                           results_vintage="",
                           results_colour="",
                           results_country="",
                           results_region="",
                           results_grape="",
                           # Credit: https://docs.mongodb.com/manual/reference/operator/aggregation/sample/
                           # Credit: https://stackoverflow.com/questions/25436630/mongodb-how-to-find-and-then-aggregate
                           carousel_one=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url":  {"$ne": ""}}},
                                        {"$sample": {"size": 1}}]),
                           carousel_two=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url": {"$ne": ""}}},
                                        {"$sample": {"size": 1}}]),
                           carousel_three=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url": {"$ne": ""}}},
                                        {"$sample": {"size": 1}}])
                           )


@app.route('/filter_regions')
def filter_regions():
    print("filter_regions")


@app.route("/search", methods=["GET", "POST"])
def search():
    # Credit: https://stackoverflow.com/questions/55617412/how-to-perform-wildcard-searches-mongodb-in-python-with-pymongo
    if request.values.get("name") == "":
        namesearch = ".*.*"
        resultname = ""
    else:
        namesearch = request.values.get("name")
        resultname = namesearch

    if request.values.get("vintage") == "":
        vintagesearch = {'$regex': '.*'}
        resultvintage = ""
    else:
        vintagesearch = request.values.get("vintage")
        resultvintage = vintagesearch

    if request.values.get("colour") == "":
        coloursearch = {'$regex': '.*'}
        resultcolour = ""
    else:
        coloursearch = request.values.get("colour")
        resultcolour = coloursearch

    if request.values.get("country") == "":
        countrysearch = {'$regex': '.*'}
        resultcountry = ""
    else:
        countrysearch = request.values.get("country")
        resultcountry = countrysearch

    if request.values.get("region") == "":
        regionsearch = {'$regex': '.*'}
        resultregion = ""
    else:
        regionsearch = request.values.get("region")
        resultregion = regionsearch

    if request.values.get("grape") == "":
        grapesearch = {'$regex': '.*'}
        resultgrape = ""
    else:
        grapesearch = request.values.get("grape")
        resultgrape = grapesearch

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    results_string = resultname + resultvintage + resultcolour + resultcountry + resultregion + resultgrape

    if not re.match("^[a-zA-Z0-9 ]+$", request.values.get("name")) and request.values.get("name") != "":
        flash('illegal text entered')
        return render_template("index.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               results_winename="",
                               results_colour=resultcolour,
                               results_country=resultcountry,
                               results_region=resultregion,
                               results_grape=resultgrape,
                               vintagenumfail=True,
                               # Credit: https://docs.mongodb.com/manual/reference/operator/aggregation/sample/
                               # Credit: https://stackoverflow.com/questions/25436630/mongodb-how-to-find-and-then-aggregate
                               carousel_one=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url":  {"$ne": ""}}},
                                               {"$sample": {"size": 1}}]),
                               carousel_two=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url": {"$ne": ""}}},
                                               {"$sample": {"size": 1}}]),
                               carousel_three=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url": {"$ne": ""}}},
                                               {"$sample": {"size": 1}}])
                               )

    if not all(char.isdigit() for char in resultvintage):
        flash('vintage must be 4 numerals')
        return render_template("index.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               results_winename=resultname,
                               results_colour=resultcolour,
                               results_country=resultcountry,
                               results_region=resultregion,
                               results_grape=resultgrape,
                               vintagenumfail=True,
                               # Credit: https://docs.mongodb.com/manual/reference/operator/aggregation/sample/
                               # Credit: https://stackoverflow.com/questions/25436630/mongodb-how-to-find-and-then-aggregate
                               carousel_one=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url":  {"$ne": ""}}},
                                               {"$sample": {"size": 1}}]),
                               carousel_two=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url": {"$ne": ""}}},
                                               {"$sample": {"size": 1}}]),
                               carousel_three=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url": {"$ne": ""}}},
                                               {"$sample": {"size": 1}}])
                               )

    if results_string == "":
        return render_template("index.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               results_winename=resultname,
                               results_vintage=resultvintage,
                               results_colour=resultcolour,
                               results_country=resultcountry,
                               results_region=resultregion,
                               results_grape=resultgrape,
                               # Credit: https://docs.mongodb.com/manual/reference/operator/aggregation/sample/
                               # Credit: https://stackoverflow.com/questions/25436630/mongodb-how-to-find-and-then-aggregate
                               carousel_one=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url":  {"$ne": ""}}},
                                               {"$sample": {"size": 1}}]),
                               carousel_two=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url": {"$ne": ""}}},
                                               {"$sample": {"size": 1}}]),
                               carousel_three=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url": {"$ne": ""}}},
                                               {"$sample": {"size": 1}}])
                               )

    resultscount = mongo.db.wines.find(
                                {"$and": [{"$or": [
                                    # Credit: https://stackoverflow.com/questions/55617412/how-to-perform-wildcard-searches-mongodb-in-python-with-pymongo
                                    {'wine_name': {'$regex': '.*' + namesearch + '.*'}},
                                    {'wine_name': {'$regex': '.*' + namesearch.title() + '.*'}}]},
                                    {"vintage": vintagesearch},
                                    {"colour": coloursearch},
                                    {"country": countrysearch},
                                    {"region": regionsearch},
                                    {"grape": grapesearch}
                                    ]})
    if resultscount.count() == 0:
        return render_template("index.html",
                               results=mongo.db.wines.aggregate(
                                                   [{"$sample": {"size": 1}}]),
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               results_winename=resultname,
                               results_vintage=resultvintage,
                               results_colour=resultcolour,
                               results_country=resultcountry,
                               results_region=resultregion,
                               results_grape=resultgrape,
                               # Credit: https://docs.mongodb.com/manual/reference/operator/aggregation/sample/
                               # Credit: https://stackoverflow.com/questions/25436630/mongodb-how-to-find-and-then-aggregate
                               carousel_one=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url":  {"$ne": ""}}},
                                               {"$sample": {"size": 1}}]),
                               carousel_two=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url": {"$ne": ""}}},
                                               {"$sample": {"size": 1}}]),
                               carousel_three=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url": {"$ne": ""}}},
                                               {"$sample": {"size": 1}}]),
                               zerocount=0
                               )

    return render_template("index.html",
                           results=mongo.db.wines.find(
                                {"$and": [{"$or": [
                                    # Credit: https://stackoverflow.com/questions/55617412/how-to-perform-wildcard-searches-mongodb-in-python-with-pymongo
                                    {'wine_name': {'$regex': '.*' + namesearch + '.*'}},
                                    {'wine_name': {'$regex': '.*' + namesearch.title() + '.*'}}]},
                                    {"vintage": vintagesearch},
                                    {"colour": coloursearch},
                                    {"country": countrysearch},
                                    {"region": regionsearch},
                                    {"grape": grapesearch}
                                    ]}),
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find(),
                           results_winename=resultname,
                           results_vintage=resultvintage,
                           results_colour=resultcolour,
                           results_country=resultcountry,
                           results_region=resultregion,
                           results_grape=resultgrape,
                           # Credit: https://docs.mongodb.com/manual/reference/operator/aggregation/sample/
                           # Credit: https://stackoverflow.com/questions/25436630/mongodb-how-to-find-and-then-aggregate
                           carousel_one=mongo.db.wines.aggregate([
                                           {"$match": {"photo_url":  {"$ne": ""}}},
                                           {"$sample": {"size": 1}}]),
                           carousel_two=mongo.db.wines.aggregate([
                                           {"$match": {"photo_url": {"$ne": ""}}},
                                           {"$sample": {"size": 1}}]),
                           carousel_three=mongo.db.wines.aggregate([
                                           {"$match": {"photo_url": {"$ne": ""}}},
                                           {"$sample": {"size": 1}}])
                           )


# Add tasting Note Routes
@app.route('/add_tasting_note_page/<wine_id>')
def add_tasting_note_page(wine_id):

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    the_wine = mongo.db.wines.find_one({"_id": ObjectId(wine_id)})
    return render_template('add_tasting_note.html',
                           wine=the_wine,
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find()
                           )


@app.route('/add_tasting_note', methods=["GET", "POST"])
def add_tasting_note():
    if request.values.get("existing_tasting_note") is None:
        tastingnoteexist = ""
    else:
        tastingnoteexist = request.values.get("existing_tasting_note")

    wineid = request.values.get("wine_id")
    tastingnotenew = request.values.get("add_tasting_note")

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    # Credit: https://stackoverflow.com/questions/15472764/regular-expression-to-allow-spaces-between-words
    if not re.match("^[a-zA-Z0-9_][a-zA-Z0-9_ ]*[a-zA-Z0-9_]$", tastingnotenew) or tastingnotenew.isnumeric():
        flash('Please enter some valid text')
        the_wine = mongo.db.wines.find_one({"_id": ObjectId(wineid)})
        return render_template('add_tasting_note.html',
                               wine=the_wine,
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find()
                               )

    ts = time.time()
    timestring = time.ctime(ts)
    tastingnoteadd = "[" + 'User: ' + session['username'] + ": " + timestring + "] " + tastingnotenew + "\r" + tastingnoteexist

    return render_template("index.html",
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find(),
                           results_winename="",
                           results_vintage="",
                           results_colour="",
                           results_country="",
                           results_region="",
                           results_grape="",
                           # Credit: https://docs.mongodb.com/manual/reference/operator/aggregation/sample/
                           # Credit: https://stackoverflow.com/questions/25436630/mongodb-how-to-find-and-then-aggregate
                           carousel_one=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url":  {"$ne": ""}}},
                                        {"$sample": {"size": 1}}]),
                           carousel_two=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url": {"$ne": ""}}},
                                        {"$sample": {"size": 1}}]),
                           carousel_three=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url": {"$ne": ""}}},
                                        {"$sample": {"size": 1}}]),
                           update=mongo.db.wines.update_one({'_id': ObjectId(wineid)},
                                                            # Credit: https://stackoverflow.com/questions/10290621/how-do-i-partially-update-an-object-in-mongodb-so-the-new-object-will-overlay
                                                            {"$set": {'tasting_notes': tastingnoteadd}}),
                           results=mongo.db.wines.find({'_id': ObjectId(wineid)})
                           )


# Edit Wine Routes
@app.route('/edit_wine_page/<wine_id>')
def edit_wine_page(wine_id):

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    the_wine = mongo.db.wines.find_one({"_id": ObjectId(wine_id)})
    return render_template('edit_wine.html',
                           wine=the_wine,
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find()
                           )


@app.route('/edit_wine/<wine_id>', methods=["GET", "POST"])
def edit_wine(wine_id):

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    nameadd = request.values.get("name")
    vintageadd = request.values.get("vintage")
    colouradd = request.values.get("colour")
    countryadd = request.values.get("country")
    regionadd = request.values.get("region")
    grapeadd = request.values.get("grape")
    if not any(char.islower() for char in nameadd):
        flash('wine name must be populated')
        return render_template("edit_wine.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               results_vintage=vintageadd,
                               results_colour=colouradd,
                               results_country=countryadd,
                               results_region=regionadd,
                               results_grape=grapeadd,
                               wine=mongo.db.wines.find_one({"_id": ObjectId(wine_id)})
                               )
    if not all(char.isdigit() for char in vintageadd):
        flash('vintage must be 4 numerals')
        return render_template("edit_wine.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               results_name=nameadd,
                               results_colour=colouradd,
                               results_country=countryadd,
                               results_region=regionadd,
                               results_grape=grapeadd,
                               wine=mongo.db.wines.find_one({"_id": ObjectId(wine_id)})
                               )
    if nameadd == "" or vintageadd == "" or colouradd == "" or countryadd == "" or regionadd == "" or grapeadd == "":
        flash('all fields must be populated')
        return render_template("edit_wine.html",
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               results_name=nameadd,
                               results_vintage=vintageadd,
                               results_colour=colouradd,
                               results_country=countryadd,
                               results_region=regionadd,
                               results_grape=grapeadd,
                               wine=mongo.db.wines.find_one({"_id": ObjectId(wine_id)})
                               )
    wines = mongo.db.wines
    existing_wine = wines.find_one({"wine_name": nameadd.title(),
                                    "vintage": vintageadd,
                                    "colour": colouradd,
                                    "country": countryadd,
                                    "region": regionadd,
                                    "grape": grapeadd,
                                    "photo_url": "",
                                    "tasting_notes": ""})

    # Credit: https://pythonprogramming.net/flash-flask-tutorial/
    flash("The wine has been updated")
    return render_template("edit_wine.html",
                           user_name=user_return,
                           insert=mongo.db.wines.update_one({'_id': ObjectId(wine_id)},
                                                            {"$set": {"wine_name": nameadd.title(),
                                                                      "vintage": vintageadd,
                                                                      "colour": colouradd,
                                                                      "country": countryadd,
                                                                      "region": regionadd,
                                                                      "grape": grapeadd}}),
                           results_winename=nameadd,
                           results_vintage=vintageadd,
                           results_colour=colouradd,
                           results_country=countryadd,
                           results_region=regionadd,
                           results_grape=grapeadd,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find(),
                           results=mongo.db.wines.find({'_id': ObjectId(wine_id)}),
                           wine=mongo.db.wines.find_one({"_id": ObjectId(wine_id)})
                           )


# Upload Image
@app.route('/upload_image_page/<wine_id>')
def upload_image_page(wine_id):

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    the_wine = mongo.db.wines.find_one({"_id": ObjectId(wine_id)})
    return render_template('image_upload.html',
                           wine=the_wine,
                           user_name=user_return
                           )


# Check For Image Extension
def allowed_image(filename):
    if "." not in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


# Upload Image
@app.route('/upload_image/<wine_id>', methods=["GET", "POST"])
def upload_image(wine_id):
    # Credit: https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python

    # Retrieve the connection string for use with the application. The storage
    # connection string is stored in an environment variable on the machine
    # running the application called AZURE_STORAGE_CONNECTION_STRING. If the environment variable is
    # created after the application is launched in a console or with Visual Studio,
    # the shell or application needs to be closed and reloaded to take the
    # environment variable into account.

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

    # Get the user unput image file Credit: https://pythonise.com/series/learning-flask/flask-uploading-files
    if request.method == "POST":
        if request.files:
            image = request.files["filename"]
            if image.filename == "":
                the_wine = mongo.db.wines.find_one({"_id": ObjectId(wine_id)})
                return render_template('image_upload.html',
                                       wine=the_wine,
                                       upload_error='No image selected',
                                       user_name=user_return
                                       )

            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
            else:
                the_wine = mongo.db.wines.find_one({"_id": ObjectId(wine_id)})
                return render_template('image_upload.html',
                                       wine=the_wine,
                                       upload_error='Incorrect file type selected - must be: "JPEG", "JPG", "PNG" or "GIF"',
                                       user_name=user_return
                                       )

    # Get static file and save to upload_images directory to upload
    local_path = "./upload_images"
    local_file_name = filename
    upload_file_path = os.path.join(local_path, local_file_name)

    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    # Set the name for the container
    container_name = "caveduvins"
    container_client = ContainerClient.from_connection_string(conn_str=connect_str, container_name=container_name)

    # Set the upload file name
    upload_file_name = wine_id + str(uuid.uuid4()) + ".jpg"

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=upload_file_name)

    # Upload the created file
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)

    # Delete the file from upload_images directory
    os.remove(upload_file_path)

    # create a url for the image
    image_url = "https://mystorageacct180671.blob.core.windows.net/" + container_name + "/" + upload_file_name
    wineid = wine_id

    flash("Image uploaded")

    return render_template("index.html",
                           update=mongo.db.wines.update({'_id': ObjectId(wineid)},
                                                        # Credit: https://stackoverflow.com/questions/10290621/how-do-i-partially-update-an-object-in-mongodb-so-the-new-object-will-overlay
                                                        {"$set": {'photo_url': image_url}}),
                           user_name=user_return,
                           colours=mongo.db.colours.find(),
                           country=mongo.db.country.find(),
                           region=mongo.db.region.find(),
                           grape=mongo.db.grape.find(),
                           results_winename="",
                           results_vintage="",
                           results_colour="",
                           results_country="",
                           results_region="",
                           results_grape="",
                           results=mongo.db.wines.find({'_id': ObjectId(wineid)}),
                           # Credit: https://docs.mongodb.com/manual/reference/operator/aggregation/sample/
                           # Credit: https://stackoverflow.com/questions/25436630/mongodb-how-to-find-and-then-aggregate
                           carousel_one=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url":  {"$ne": ""}}},
                                        {"$sample": {"size": 1}}]),
                           carousel_two=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url": {"$ne": ""}}},
                                        {"$sample": {"size": 1}}]),
                           carousel_three=mongo.db.wines.aggregate([
                                        {"$match": {"photo_url": {"$ne": ""}}},
                                        {"$sample": {"size": 1}}])
                           )


# View Image
@app.route('/view_image_page/<wine_id>')
def view_image_page(wine_id):

    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'

    return render_template("view_image.html",
                           user_name=user_return,
                           wine=mongo.db.wines.find({'_id': ObjectId(wine_id)})
                           )


# My Profile
@app.route('/my_profile_page/')
def my_profile_page():
    if 'username' in session:
        user_return = 'User: ' + session['username']
        added_by = session['username']
        if session['username'] == 'admin':
            return render_template("my_profile.html",
                                   user_name=user_return,
                                   added_by=added_by,
                                   results=mongo.db.wines.find(),
                                   notes=mongo.db.wines.find(
                                       {"$or": [
                                           {'tasting_notes': {'$regex': '.*' + added_by + '.*'}},
                                           {'tasting_notes': {'$regex': '.*' + added_by.title() + '.*'}}]}
                                           )
                                   )
        return render_template("my_profile.html",
                               user_name=user_return,
                               added_by=added_by,
                               results=mongo.db.wines.find({'added_by': added_by}),
                               notes=mongo.db.wines.find(
                                   {"$or": [
                                       {'tasting_notes': {'$regex': '.*' + added_by + '.*'}},
                                       {'tasting_notes': {'$regex': '.*' + added_by.title() + '.*'}}]}
                                       )
                               )
    else:
        user_return = 'Cave du Vins'
        return render_template('index.html',
                               user_name=user_return,
                               colours=mongo.db.colours.find(),
                               country=mongo.db.country.find(),
                               region=mongo.db.region.find(),
                               grape=mongo.db.grape.find(),
                               results_winename="",
                               results_vintage="",
                               results_colour="",
                               results_country="",
                               results_region="",
                               results_grape="",
                               # Credit: https://docs.mongodb.com/manual/reference/operator/aggregation/sample/
                               # Credit: https://stackoverflow.com/questions/25436630/mongodb-how-to-find-and-then-aggregate
                               carousel_one=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url": {"$ne": ""}}},
                                               {"$sample": {"size": 1}}]),
                               carousel_two=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url": {"$ne": ""}}},
                                               {"$sample": {"size": 1}}]),
                               carousel_three=mongo.db.wines.aggregate([
                                               {"$match": {"photo_url": {"$ne": ""}}},
                                               {"$sample": {"size": 1}}])
                               )

if __name__ == '__main__':
    app.static_folder = 'static'
    app.secret_key = os.environ.get("SECRET_KEY")
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=False)
