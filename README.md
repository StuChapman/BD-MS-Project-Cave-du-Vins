# Cave du Vins – An online cellar of fine wine

Link to the deployed wesite [here](https://bd-ms-project-cave-du-vins.herokuapp.com/)

# Introduction

Create a web application that stores, organises and presents a multi-user input and updated collection of wine; 
including:
1.  Wine Name (free text - capitalised on input)
2.  Vintage (4 digits)
3.  Colour (selected from a list for data cleanliness)
4.  Country (selected from a list for data cleanliness)
5.  Region (selected from a list for data cleanliness)
6.  Grape (selected from a list for data cleanliness)
7.  Tasting Notes (free text)
8.  A user-uploaded image of the wine

The lists for: Colour, Country, Region and Grape are held in seperate collections in the database. 
These collections can be added to by registered users (i.e. as a wine is added from a country not listed).
Documents can be deleted from the collections only by the administrator; through a seperate log in.

# UX

The app should be designed ‘mobile first’, and should be equally as accessible through desktop and laptop devices.
User Stories are organised in the following groups:
* Registration
* Logging in
* Browsing
* Adding Wines
* Updating Wine Information
* Navigation
* Administrator access (credentials can be found in [admin-credentials.txt](https://github.com/StuChapman/BD-MS-Project-Cave-du-Vins/blob/987cf88bda8f97f9b421680e54477c323c8be3f7/admin-credentials.txt))

## User Stories 

### Registration
As a user of Cave du Vins, I …
1.  … want to be able to register a username and password.
2.  … want my password to be secure.
### Logging In
As a registered user of Cave du Vins, I …
1.  … want to be able to access further functionality by logging in.
2.  … want to be able to log out of the application.
### Browsing
As a user of Cave du Vins, I …
1.  … want to be able to browse the collection of wines by:
    * Wine Name - by full title, partial title/word, upper-case or lower-case.
    * Vintage (e.g. all wines in the collection produced in 1999).
    * Colour (e.g. Red, White or Rose).
    * Country (e.g. all wines in the collection produced in France).
    * Region (e.g. all wines in the collection produced in the Bordeaux region).
    * Grape (e.g. all wine in the collection produced from the Cabernet Sauvignon grape variety).
2.  … want the browsed wines to be presented to me in a list.
3.  … want to be able to navigate to a site where I can purchase the wines in the database.
### Adding Wines
As a registered user of Cave du Vins, I …
1.  … want to be able to add wines to the database.
2.  … want to be able to add colours to the database.
3.  … want to be able to add countries to the database.
4.  … want to be able to add regions to the database.
5.  … want to be able to add grape varieties to the database.
6.  … want any uploaded images of the wines I add to the database.
### Updating Wine Information
As a registered user of Cave du Vins, I …
1.  … want to be able to add tasting notes to the database.
2.  … want to be able to alter and append tasting notes in the database.
3.  … want to be able to upload images of wines to the database.

As an administrator of Cave du Vins, I …
1.  … want to be able to delete wines from the database.
2.  … want to be able to remove colours from the database.
3.  … want to be able to remove countries from the database.
4.  … want to be able to remove regions from the database.
5.  … want to be able to remove grape varieties from the database.
### Navigation
As a user of Cave du Vins, I …
1.  … want to be able to navigate to the different functions easily, from any area of the application.
2.  … want to be able to navigate anywhere on the application without the use of the browser's navigation.

As a registered user of Cave du Vins, I also …
1.  … want to be able to be able to navigate to additional features on the application reserved for registered users.
As an administrator of Cave du Vins, I also …
2.  … want to be able to be able to navigate to additional features on the application reserved for administrators.

## Validation

As there are multiple data entry features on the application, I created validation rules (some credited to other developers)
to ensure that data is consistent within the database.

### Registration
1.  Password should be at least 6 characters.
2.  Password should be no more than 10 characters.
3.  Password should have at least one numeral.
4.  Password should have at least one uppercase letter.
5.  Password should have at least one lowercase letter.
6.  Password should have at least one of the symbols $, @, #, % or !.
7.  User name must be unique and not already present in the users collection.
8.  User name must consist of text and numbers, with no spaces.

The code for requirements Validation-Registration:1-7 is credited to: [geeksforgeeks](https://www.geeksforgeeks.org/password-validation-in-python/#:~:text=Conditions%20for%20a%20valid%20password%20are%3A%201%20Should,be%20between%206%20to%2020%20characters%20long.%20)

The code for requirements Validation-Registration:8 is credited to: [stackoverflow](https://stackoverflow.com/questions/15580917/python-data-validation-using-regular-expression)

### Logging In
1.  User name and password must match a document in the users collection.

### Browsing
1.  Wine Name has no validation.
2.  Vintage must be 4 characters.
3.  Colour must be selected from a list.
4.  Country must be selected from a list.
5.  Region must be selected from a list.
6.  Grape must be selected from a list.

### Adding Wines
1.  Wine Name must be populated.
2.  Vintage must be 4 numerals.
3.  All fields must be populated.
4.  Colour must be selected from a list.
5.  Country must be selected from a list.
6.  Region must be selected from a list.
7.  Grape must be selected from a list.

### Updating Wine Information
1.  Tasting Notes are limited to 500 characters.
2.  Country must include at least 1 character.
3.  Country must be unique and not already present in the country collection
4.  Region must include at least 1 character.
5.  Region must be unique and not already present in the region collection
6.  Grape must include at least 1 character.
7.  Grape must be unique and not already present in the grape collection
8.  Image must have a name.
9.  Image file type must be one of: "JPEG", "JPG", "PNG" or "GIF".

The code for requirements Validation-Updating-Wine-Information:8-9 is credited to: [pythonise](https://pythonise.com/series/learning-flask/flask-uploading-files)

### Navigation
1. Only a registered user or administrator can access the Add Wine button.
2. Only a registered user or administrator can access the Tasting Notes button.
3. Only a registered user or administrator can access the Upload Image button.
4. Only an administrator can access the Delete Wine button.
5. Only an administrator can access the delete country ("-Del") button.
6. Only an administrator can access the delete region ("-Del") button.
7. Only an administrator can access the delete grape ("-Del") button.

## Mockups:

As is now standard workflow for me; I produced detailed mockups for: phones, tablets and desktop devices prior to writing any code. Key design decisions are made at this stage to ensure the creation of code meets these designs, rather than designing the app at the same time as coding it.
I included the data structure for the backend databases in the mockups.

[phone](https://github.com/StuChapman/BD-MS-Project-Cave-du-Vins/blob/987cf88bda8f97f9b421680e54477c323c8be3f7/mockups/Data-Centric%20Development%20Milestone%20Project%20%28phone%29.jpg)

[tablet](https://github.com/StuChapman/BD-MS-Project-Cave-du-Vins/blob/987cf88bda8f97f9b421680e54477c323c8be3f7/mockups/Data-Centric%20Development%20Milestone%20Project%20%28tablet%29.jpg)

[laptop](https://github.com/StuChapman/BD-MS-Project-Cave-du-Vins/blob/987cf88bda8f97f9b421680e54477c323c8be3f7/mockups/Data-Centric%20Development%20Milestone%20Project%20%28desktop%29.jpg)

I used [figma](https://www.figma.com/) to produce the mockups. 

### Colour Schemes and Fonts

The core scheme of the app is the 'One Page Wonder' theme from [start bootstrap](https://startbootstrap.com/theme/one-page-wonder)

I also used this [image](https://github.com/StuChapman/BD-MS-Project-Cave-du-Vins/blob/master/static/img/IMG_4723sml.JPG) 
as a background image throughout the app, and picked up 2 colours from wine bottle capsules, by eyedropping to get the hex code.

1. #FFD374 for yellow
2. #2E9693 for blue

These colours were used on buttons across the app to deliver a consistent experience.

The fonts used in 'One Page Wonder' are:
 
 1. font-family: 'Lato'
 2. font-family: 'Catamaran'

I used these fonts exclusively.

## Features

### Existing Features

#### Navigation
1. A navigation bar, collapsed to burger menu for mobile devices.
2. A "Home" hyperlink that displays "Cave du Vins" if the user is not signed in, or the username if they are signed in"
3. An menu of: Sign up, Log in/out, Browse wines and Add wine (only enabled for signed in users)
#### Home Page
1. A "Browse wines" hyperlink to navigate to a bookmark at the top of the browse wines form.
2. A browse wines form with the option to search on: wine name, vintage, colour, country, region and grape
3. Colour, country, region and grape are pre-populated select inputs.
4. A Search button to return wines that match the search.
5. A Reset button to clear the browse form.
6. The number of wines returned that match the search criteria.
7. The wines listed that meet the search criteria showing: vintage, colour, country, region, tasting notes (if populated), image (if populated).
8. A button to add tasting notes (only enabled for signed in users).
9. A button to upload image (only enabled for signed in users).
10. A button to delete win (only enabled for administrators).
11. A button to buy this wine (by opening a search of the wine and vintage in [winesearcher.com](https://www.wine-searcher.com/)).
#### Upload Images
1. A file select to choose an image from the user's device.
2. A Container ("caveduvins") in [Azure](https://azure.microsoft.com/en-gb/) to host the images.
3. A URL written to the tasting_notes field in the MongoDB backend database.
#### Registration Page
1. A username input.
2. A password input.
3. A Register button to check inputs and add to the [MongoDB](https://www.mongodb.com/) database.
4. Information on the acceptance criteria for Password.
5. An error notification if the acceptance criteria for Username or Password are not met.
#### Log in Page
1. A username input.
2. A password input.
3. A Log in button to check inputs against the [MongoDB](https://www.mongodb.com/) database.
4. A link to the Registration page.
5. An error notification if the Username or Password do not match those in the [MongoDB](https://www.mongodb.com/) database.
#### Add Wine Page
1. An Add Wines form with the option to populate: wine name, vintage, colour, country, region and grape
2. Colour, country, region and grape are pre-populated select inputs.
3. An Add Wine button to input documents into the [MongoDB](https://www.mongodb.com/) database.
4. A Reset button to clear the add wine form.
5. A button to open a modal with a free text input to add a Country to the collection.
6. A button to open a modal with a free text input to add a Region to the collection.
7. A button to open a modal with a free text input to add a Grape to the collection.
8. A button to remove a Country from the collection.
9. A button to remove a Region from the collection.
10. A button to remove a Grape from the collection.
#### Edit Wine Page
1. An Edit Wines form with the option to edit: wine name, vintage, colour, country, region and grape
2. Colour, country, region and grape are pre-populated select inputs.
3. A Save button to update documents in the [MongoDB](https://www.mongodb.com/) database.
#### Delete Category page
1. A pre-populated select input to delete a: Country, Region or Grape from the respective collection.
#### View Image page
1. A full page version of the image.
2. A Back button to return to the previous search results.
#### Add Tasting Notes page
1. The current tasting note as read only.
2. A text input to allow the user to add 155 characters of free text (stamped with the username).
3. A Save button to append documents in the [MongoDB](https://www.mongodb.com/) database.

### Features Left to Implement
1.  Filter Regions on Country. As this would normally be actioned using 
    ```js 
    "onchange" 
    ```
    which triggers Javascript code, not Python, I will address this in a future iteration.

### Approach

The approach I took for designing the site, was to build on the [start bootstrap](https://startbootstrap.com/theme/one-page-wonder) 
one-page-wonder template, for small media devices in portrait view.

I added additional styling in [style.css](https://github.com/StuChapman/BD-MS-Project-Cave-du-Vins/blob/master/static/css/style.css).

I also re-used, from a Stack Overflow [discussion](https://stackoverflow.com/questions/43589507/how-can-you-have-bootstrap-responsiveness-based-on-screen-ratio-instead-of-scree),
the concepts of:
* @media screen and (orientation: portrait), and
* @media screen and (orientation: landscape)

## Technologies Used

1.  [html](https://en.wikipedia.org/wiki/HTML) - to create the structure and text of each page.
2.  [css](https://en.wikipedia.org/wiki/Cascading_Style_Sheets) - to style each page centrally and individually.
3.  [javascript](https://en.wikipedia.org/wiki/JavaScript) - was used to power the Bootstrap functionality.
4.  [jquery](https://jquery.com/) - was used to power the Bootstrap functionality.
5.  [Python](https://www.python.org/) - for interactions between the app, the MongoDB database and the Azure cloud storage.
6.  [Bootstrap](https://getbootstrap.com/) plugins - Responsive grid and prebuilt components to enable more responsive design; particularly “accordion” and “toggle” collapsed (hidden) content.
7.  [Font Awesome](https://fontawesome.com/v4.7.0/icons/) - for icons.
8.  [Figma](http://www.figma.com) - to produce the mockups.
9.  [w3 validator](https://validator.w3.org/) - for html validation.
10. [http://pep8online.com/](http://pep8online.com/) - for Python validation.
11. [Heroku](https://www.heroku.com/) - for the back end database.
12. [Azure](https://azure.microsoft.com/en-gb/) - for cloud storage to host the uploaded images.
13. [Flask](https://en.wikipedia.org/wiki/Flask_%28web_framework%29) - to provide a web framework.
14. [Pytest](https://docs.pytest.org/en/latest/index.html) - for automated test scripts.

### Backend databases

The 2 databases I created are:
1.  [MongoDB](https://github.com/StuChapman/BD-MS-Project-Cave-du-Vins/blob/4eb557a961a48780253c2ce7a88787b0db5aaf55/backend_screenshots/MongoDB.png)
2.  [Azure](https://github.com/StuChapman/BD-MS-Project-Cave-du-Vins/blob/4eb557a961a48780253c2ce7a88787b0db5aaf55/backend_screenshots/Azure.png)

MongoDB hold the main Collections: wines, users, colours, countries, grapes and regions.
Azure has a single Container (caveduvins) to host the uploaded images.

### Add ins
Within the run.py app, I installed a number of add ins to enable various capabilities:
1.  [os](https://docs.python.org/3/library/os.html#module-os) - for interaction with the operating system (e.g. retrieving the content of env.py to connect to the MongoDB backend).
2.  [Flask](https://en.wikipedia.org/wiki/Flask_%28web_framework%29), render_template, redirect, request, url_for, session, flash from flask - to provide a web framework.
3.  [PyMongo](https://pymongo.readthedocs.io/en/stable/), from flask_pymongo - to enable Python to work with MongoDB.
4.  [ObjectId](https://docs.mongodb.com/manual/reference/method/ObjectId/), from bson.objectid - to enable Python to work with MongoDB.
5.  [bcrypt](https://en.wikipedia.org/wiki/Bcrypt) - to encrypt passwords.
6.  [re](https://docs.python.org/3/library/re.html) - to utilise regular expressions in data validation.
7.  [uuid](https://docs.python.org/3/library/uuid.html) - to append a random string to the end of the upload image filename (upload_file_name = wine_id + str(uuid.uuid4()) + ".jpg").
8.  [BlobServiceClient](https://docs.microsoft.com/en-us/dotnet/api/azure.storage.blobs.blobserviceclient?view=azure-dotnet), [BlobClient](https://docs.microsoft.com/en-us/dotnet/api/azure.storage.blobs.blobclient?view=azure-dotnet), [ContainerClient](https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.containerclient?view=azure-python), '__version__', from azure.storage.blob - to interact the app with Azure.
9.  [ResourceExistsError](https://docs.microsoft.com/en-us/python/api/azure-core/azure.core.exceptions.resourceexistserror?view=azure-python), from azure.core.exceptions - to identify if a blob for the image already exists in the container.
10. [secure_filename from werkzeug.utils](https://werkzeug.palletsprojects.com/en/1.0.x/utils/?highlight=secure_filename#werkzeug.utils.secure_filename) -to add protection from malicious use when uploading an image.

## Testing
I created a separate [testing](https://github.com/StuChapman/BD-MS-Project-Cave-du-Vins/blob/733c885efed6503fffda533463fd2f32714f1ee3/testing) folder containing pre and post test matrices.

As usual; an organised testing matrix proved invaluable. Taking a disciplined approach to testing all features on all devices and browsers, 
in both portrait and landscape orientation **always** reveals unforseen issues.

Testing revealed some issues with rendering - particularly on add_tasting_note.html in landscape viw on small mobile devices,
and a number of views on Glalaxy Fold in landscape.

There was also an error with the code to navigate back to the search view from view_image.html on Edge and Opera browsers... 
*onclick="window.history.back();location.reload(); return false;"*

These were corrected in a post-testing commit.

### Automated Testing
I used [Pytest](https://docs.pytest.org/en/latest/index.html) for automated testing. Primarily for data entry validation.

To install Pytest, in the GitPod command line, enter...

pip install -U pytest

Then to run the test scripts, in the GitPod command line, enter ...

pytest

This proved particularly useful when testing the validation of user entry into the wine name input from index.html into the search() route.

I had used validation to prevent the user inputing any special characters (especially with malicious intent), but I was still permitting the input of a single "*", which cased an error.

By testing the input of "*", I saw that my code 
```{python}
if not re.match("^[a-zA-Z0-9* ]+$", request.values.get("name")):
```
should read...
```{python}
if not re.match("^[a-zA-Z0-9 ]+$", request.values.get("name")):
```
This removed the error.

### Bugs, Challenges and Errors

**IMPORTANT NOTE:**

There were 2 serious bugs when building the application.
The first was when deploying the application to [Heroku](https://www.heroku.com/). The Procfile appears to have been 
corrupted or incorrectly created, delivering an error "no web processes running". There is some discussion on the 
topic [here](https://stackoverflow.com/questions/41804507/h14-error-in-heroku-no-web-processes-running). 
On inspection of the app in Heroku, I saw that no Dyno had been added and there was the suggestion that a Procfile should be created. 
No amount of removing and rebuilding the Procfile would remove this error, so I decided to download a zip file of all the files in my 
GitHub repository, create a new repository, upload the files and rebuild the Procfile. This solved the problem. 

The second bug happened when opening the repository in Gitpod. I recieved the question "start with default docker file?". In doing so, 
The repository would not open up a PORT correctly and this error passed through to Heruko. I decided that the github docker file 
had somehow been corrupted, so again, I took the approach of creating a new repository with a new, working docker file.

The 2 redundant repositories are:

[broken Procfile](https://github.com/StuChapman/BD-MS-Project-Cave-du-Vins-broken-Procfile)

[broken Dockerfile](https://github.com/StuChapman/BD-MS-Project-Cave-du-Vins-broken-Dockerfile)

**The commit history of the entire project can be viewed in these repositories.**

1.  When designing the layout for the search form, I moved the search button outside the <form></form> - this resulted in the search criteria not being passed to the flask app. I corrected this by returning the button to the form, and finding a better way to achieve the layout I wanted.
2.  The default values in the search inputs were being passed into the flask app and preventing the code from running - I removed these.
3.  The username was resetting to 'Cave du Vins' whilst navigating around the app - I corrected this by adding the following 'if' statement and always passing the username back with render_template...
```{python}
    if 'username' in session:
        user_return = 'User: ' + session['username']
    else:
        user_return = 'Cave du Vins'
    return render_template('login.html', 
                            user_name = user_return)
```
4.  I needed to be able to allow the user to search wine_name using a lower or uppercase string  - I achieved this with the help of [stack overflow](https://stackoverflow.com/questions/55617412/how-to-perform-wildcard-searches-mongodb-in-python-with-pymongo), and the following code...
```{python}
[{"$or": [
    {'wine_name': {'$regex': '.*' + namesearch + '.*'}},
    {'wine_name': {'$regex': '.*' + namesearch.title() + '.*'}}]
```
5.  I had an issue where searching on totally blank search fields returned the complete collection - I created a string to check for complete blank and returned to the pre-populated search form...
```{python}
    results_string = resultname + resultvintage + resultcolour + resultcountry + resultregion + resultgrape

    if results_string == "":
        return render_template("index.html", 
                                user_name = user_return, 
                                colours=mongo.db.colours.find(), 
                                country=mongo.db.country.find(), 
                                region=mongo.db.region.find(), 
                                grape=mongo.db.grape.find(),
                            )
```
6.  I created an issue by passing my code through the Python validator, and slavishly following the protocols. I determined to use the validator carefully from then on.
    Specifically I decided to be relaxed about lines that are over 79 characters in length. My research suggests this is a recommendation, rather than an error. In future, I will learn more methods of breaking up lines of code.
7.  I had the issue with the broken Procfile as detailed above.
8.  I had a bug where the search fields were populated with a default values after deleting a wine. They should be return to blank - I used code to clear each of the variables...
```{python}
    delete=mongo.db.wines.remove({'_id': ObjectId(wine_id)})
    results_winename="",
    results_vintage="",
    results_colour="",
    results_country="",
    results_region="",
    results_grape=""
    )
```
9.  I had the issue with the broken Dockerfile as detailed above.
10. I had left the default value "select" in the select inputs on add_wine.html. This caused the fileds to reset after the wine was added, but a much better user experience was to have the new wine returned.
11. There was also an issue with the GutHub repository not updating with the latest code pushed from GitPod. The GitPod workspace had been upversioned and commited over 5 days, but none of these reflected in the repository. I manually updated the repository to consolidation all updates.
12. There was an issue with the rendering of the app under https. There are 2 articles here [stackoverflow.com](https://stackoverflow.com/questions/7918394/why-images-and-css-do-not-show-under-https) and here [stackoverflow.com](https://stackoverflow.com/questions/13772884/css-problems-with-flask-web-app). I found that a combination of:
    * adding ```{python}app.static_folder = 'static'``` to ```{python} if __name__ == '__main__':``` and
    * changing the hrefs for css stylesheets to absolute filepaths, solved the problem.
13. There same issue applied to the src paths for bootstrap javascript. Again changing to absolute file paths corrected this.
14. A friend of mine, [Magoo](https://www.facebook.com/carlos.fandango.56232), who works in IT, had a play with the app and created an error by attempting to inject SQL into the text input for wine name on index.html. I added validation for non alphanumeric text to avoid this happening. Thanks Magoo!

Apart from the 2 major isses with Procfile and Dockefile; the most challenging aspect of the project was uploading images to cloud storage.

I found this [tutorial: storage-quickstart-blobs-python](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python) whiched helped me to upload a static image.
But I needed the image to be dynamically selected by the user from thier device.
This [tutorial: flask-uploading-files](https://pythonise.com/series/learning-flask/flask-uploading-files) showed me how to use flask to upload a user selected file into a static folder.
I then blended the 2 bits of code together to upload the user selected image to a static folder, then upload the image from the static folder to the cloud.

This didn't feel like the most elegant of solutions, but it is effective.

### Code Validators

Screenshots of the recommendations of the validators are:
[PEP8 - python](https://github.com/StuChapman/BD-MS-Project-Cave-du-Vins/blob/6db5f03f85eca8dc70943c67aa5fe8df8a94baa4/validation_screenshots)

## Additional Features post Testing
Following user testing with my mentor [Precious Ijege](https://www.linkedin.com/in/precious-ijege-908a00168/) and my 
friend [Magoo](https://www.facebook.com/carlos.fandango.56232), I added the following features...

1.  A [Bootstrap](https://getbootstrap.com/) Carousel showing 3 randomly selected wines, with image to start the user's browsing journey.
2.  A My Profile page for individual users to see the wines they have:
    * Added
    * Contributed to the Tasting Notes of
    I also redesigned how wines could be edited and deleted using these views.
    (Note: user:admin can view/edit and delete all wines).
3.  A wine "recommended" (randomly selected) if the user creates a search that returns zero documents.
4.  A timestamp on Tasting Notes.
5.  An 'Edit own wines' feature.

### Solutions to User Stories

### Registration
As a user of Cave du Vins, I …
1.  … want to be able to register a username and password.
2.  … want my password to be secure.
### Logging In
As a registered user of Cave du Vins, I …
1.  … want to be able to access further functionality by logging in.
2.  … want to be able to log out of the application.
### Browsing
As a user of Cave du Vins, I …
1.  … want to be able to browse the collection of wines by:
    * Wine Name - by full title, partial title/word, upper-case or lower-case.
    * Vintage (e.g. all wines in the collection produced in 1999).
    * Colour (e.g. Red, White or Rose).
    * Country (e.g. all wines in the collection produced in France).
    * Region (e.g. all wines in the collection produced in the Bordeaux region).
    * Grape (e.g. all wine in the collection produced from the Cabernet Sauvignon grape variety).
2.  … want the browsed wines to be presented to me in a list.
3.  … want to be able to navigate to a site where I can purchase the wines in the database.
### Adding Wines
As a registered user of Cave du Vins, I …
1.  … want to be able to add wines to the database.
2.  … want to be able to add colours to the database.
3.  … want to be able to add countries to the database.
4.  … want to be able to add regions to the database.
5.  … want to be able to add grape varieties to the database.
6.  … want any uploaded images of the wines I add to the database.
### Updating Wine Information
As a registered user of Cave du Vins, I …
1.  … want to be able to add tasting notes to the database.
2.  … want to be able to alter and append tasting notes in the database.
3.  … want to be able to upload images of wines to the database.

As an administrator of Cave du Vins, I …
1.  … want to be able to delete wines from the database.
2.  … want to be able to remove colours from the database.
3.  … want to be able to remove countries from the database.
4.  … want to be able to remove regions from the database.
5.  … want to be able to remove grape varieties from the database.
### Navigation
As a user of Cave du Vins, I …
1.  … want to be able to navigate to the different functions easily, from any area of the application.
2.  … want to be able to navigate anywhere on the application without the use of the browser's navigation.

As a registered user of Cave du Vins, I also …
1.  … want to be able to be able to navigate to additional features on the application reserved for registered users.
As an administrator of Cave du Vins, I also …
2.  … want to be able to be able to navigate to additional features on the application reserved for administrators.


## Deployment

I deployed to Heroku by the following steps:
1.  Create a new Heroku app.
2.  Click on "Reveal Config Vars" to add any hidden environment variables.
3.  Add the key of "IP" and the value of "0.0.0.0", and click on Add.
4.  Add the key of "PORT" and the value of "5000", then click Add.
5.  Add the key of "MONGO_URI" and the value of "*...this is the connection string for the MongoDB database...*", then click Add to connect to MongoDB
6.  Add the key of "AZURE_STORAGE_CONNECTION_STRING" and the value of "*...this is the connection string for the Azure database...*", then click Add to connect to Azure.
7.  Add the key of "SECRET_KEY" and the value of "*...this is the secret_key for the app...*", then click Add to set.
8.  Set the app to automatically deploy from GitHub by selecting GitHub on the Deploy tab.
9.  Enter the repository name (BD-MS-Project-Cave-du-Vins) and click Search.
10. Click Connect next to the repository name.

To push to Heroku from GitPod (from the command line...)
1.  pip3 freeze --local > requirements.txt to create a requirements file.
2.  echo web: python run.py > Procfile to create a Procfile.
3.  npm install -g heroku
4.  heroku login -i (enter Heroku credentials)
5.  git remote add heroku https://git.heroku.com/bd-ms-project-cave-du-vins.git
6.  heroku ps:scale web=1
7.  git push -u heroku master

#### To run the code locally;

1.  From the BD-MS-Project-Cave-du-Vins repository in Github, click ‘Clone or download’.
2.  Copy the URL to your clipboard.
3.  In Gitpod, open the terminal.
4.  Change the directory to that where you wish to place the files.
5.  Type ‘git clone’ then paste the URL.

#### To run the code in Gitpod;

1. Create a file env.py, containing the code...

    import os

    os.environ.setdefault(*...this is the connection string for the MongoDB database...*)
    os.environ.setdefault("MONGO_DBNAME", '*...this is the MongoDB database name...*')
    os.environ.setdefault("SECRET_KEY", '*...this is the secret_key for the app...*')

2.  Type into the command line:
    * pip3 install flask_pymongo
    * pip3 install pymongo
    * pip3 install flask
    * pip3 install bcrypt
    * pip3 install dnspython
    * pip install azure-storage-blob
    * export AZURE_STORAGE_CONNECTION_STRING="*...this is the connection string for the Azure database...*"
    * python3 run.py

## Credits

### Content

1.  Template from [start bootstrap](https://startbootstrap.com/theme/one-page-wonder)
2.  The method for aligning text vertically is from [webdevblog](www.webdevblog.com/css-vertical-align/) 
3.  @media screen and (orientation: portrait) and (orientation: landscape) from [stackoverflow.com](https://stackoverflow.com/questions/43589507/how-can-you-have-bootstrap-responsiveness-based-on-screen-ratio-instead-of-scree).
4.  Creating a user registration and log in system is from [edubanq.com](https://edubanq.com/programming/mongodb/creating-a-user-login-system-using-python-flask-and-mongodb/)
5.  Logging out as a user is from [pythonbasics.org](https://pythonbasics.org/flask-sessions/)
6.  Data validation using regular expression is from [stackoverflow.com](https://stackoverflow.com/questions/15580917/python-data-validation-using-regular-expression)
7.  Password validation in Python is from [www.geeksforgeeks.org](https://www.geeksforgeeks.org/password-validation-in-python/#:~:text=Conditions%20for%20a%20valid%20password%20are%3A%201%20Should,be%20between%206%20to%2020%20characters%20long.%20)
8.  Using 'flash' to sent messages to the user is from [pythonprogramming.net](https://pythonprogramming.net/flash-flask-tutorial/)
9.  Performing wildcard seaches in Pymongo is from [stackoverflow.com](https://stackoverflow.com/questions/55617412/how-to-perform-wildcard-searches-mongodb-in-python-with-pymongo)
10. Updating a single field in a collection is from [stackoverflow.com](https://stackoverflow.com/questions/10290621/how-do-i-partially-update-an-object-in-mongodb-so-the-new-object-will-overlay)
11. Uploading an image to Azure from Python is from [docs.microsoft.com](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python)
12. Getting a user input file in Flask is from [pythonise.com](https://pythonise.com/series/learning-flask/flask-uploading-files)
13. Setting background image opacity is from [coder-coder.com](https://coder-coder.com/background-image-opacity/)
14. Validating tasting notes input is from [stackoverflow.com](https://stackoverflow.com/questions/15472764/regular-expression-to-allow-spaces-between-words)
15. Error handling is from [askpython.com](https://www.askpython.com/python-modules/flask/flask-error-handling)
16. Random sampling of records is from [docs.mongodb.com](https://docs.mongodb.com/manual/reference/operator/aggregation/sample/)
17. Aggregate on a select set of records is from [stackoverflow.com](https://stackoverflow.com/questions/25436630/mongodb-how-to-find-and-then-aggregate)

### Media

1.  All images were taken by me.

### Acknowledgements

I would like to thank the following people for thier support and input:

1. As always, my mentor, [Precious Ijege](https://www.linkedin.com/in/precious-ijege-908a00168/) who teaches me the details that stay with me, like - never work on your code on the morning of a live demo!!!
2. My friends [Scott](https://www.facebook.com/scott.mckellar.399) and [Magoo](https://www.facebook.com/carlos.fandango.56232), who I consulted before I started the FSD course, and gave me the confidence to go for it!


