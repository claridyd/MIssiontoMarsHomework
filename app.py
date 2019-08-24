# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Create connection variable
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    # query Mongo db and pass into HTML template
    mars_info = mongo.db.collection.find_one()
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scrape():

    # Run the scrape function
    Mars_scrape = scrape_mars.scrape()

    # Update Mongo database 
    mongo.db.collection.update({}, Mars_scrape, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
     app.run(debug=True)
