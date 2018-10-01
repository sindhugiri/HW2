## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################

from flask import Flask, request, flash, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

import requests 
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'
app.debug=True

####################
###### FORMS #######
####################

class AlbumEntryForm (FlaskForm): 
    header = StringField("Enter the name of an album:", validators =[Required()])
    ranking = RadioField("How much do you like this album? (1 low, 3 high)", choices=[("1","1"), ("2","2"), ("3","3")])
    submit = SubmitField("Submit")

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/user/<name>')
def hello_user(name):
	return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistinfo', methods=["GET"])
def example_1():
    if request.method == "GET":
        term = request.args.get("artist", "nothing")
        params = {}
        params["term"] = term
        response = requests.get("https://itunes.apple.com/search", params=params)
        data = json.loads(response.text)
        r = data["results"]
    return render_template('artist_info.html', objects=r)

@app.route('/artistlinks')
def example_2():
	return render_template("artist_links.html")

@app.route('/artistform', methods = ['GET'])
def example_3():
	return render_template('artistform.html')

@app.route('/specific/song/<artist_name>')
def example_4(artist_name):
    params = {}
    params["term"] = artist_name
    response = requests.get("https://itunes.apple.com/search", params=params)
    data = json.loads(response.text)
    r = data["results"]
    return render_template("specific_artist.html", results=r)

@app.route('/album_entry')
def example_5():
    form=AlbumEntryForm()
    return render_template("album_entry.html", form=form)

@app.route('/album_result', methods=["GET", "POST"]) 
def example_6():
    if request.method == "GET":
        form = AlbumEntryForm()
        header=form.header.data
        ranking=form.ranking.data
        return render_template("album_data.html", header=header, ranking=ranking)
    return ("No Data!")

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
