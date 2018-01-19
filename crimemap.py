#coding:utf-8
from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import json

app = Flask(__name__)
DB = DBHelper()

@app.route('/')
def home():
    try:
        crimes = DB.get_all_crimes()
        crimes = json.dumps(crimes)
    except Exception as e:
        print e
        crimes = None
    return render_template('home.html', crimes=crimes)

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
    date = request.form.get('date')
    print date
    latitude = float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))
    description = request.form.get('description')
    DB.add_crime(category, date, latitude, longitude, description)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
