#coding:utf-8
from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import string
import datetime
import dateparser
import json

app = Flask(__name__)
DB = DBHelper()

categories = ['mugging', 'break-in']

@app.route('/')
def home(error_message = None):
    try:
        crimes = DB.get_all_crimes()
        crimes = json.dumps(crimes)
    except Exception as e:
        print e
        crimes = None
    return render_template('home.html', crimes=crimes, categories=categories, error_message = error_message)

@app.route('/add', methods = ['POST'])
def add():
    try:
        data = request.form.get('userinput')
        DB.add_input(data)
    except Exception as e:
        print e
    return home()

@app.route('/clear')
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print e
    return home()

@app.route('/submitcrime', methods=['POST'])
def submitcrime():
    category = request.form.get('category')
    if category not in categories:
        return home()
    date = format_date(request.form.get('date'))
    if not date:
        return home('Invalid date. Please use yyyy-mm-dd format')
    try:
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))
    except ValueError:
        return home()
    description = request.form.get('description')
    description = sanitize_string(description)
    DB.add_crime(category, date, latitude, longitude, description)
    return home()

def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None

def sanitize_string(userinput):
    whitelist = string.letters + string.digits + '!@#$%^&*() '
    return filter(lambda x:x in whitelist, userinput)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
