from flask import Flask
import math
from flask import url_for, render_template, request, redirect, request
import sqlite3

#from model import *
from search_func import *

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instabase.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db.app = app
#db.init_app(app)

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/how_to', methods = ['GET'])
def how_to():
        return render_template('how_to.html')

@app.route('/results', methods = ['GET'])
def results():
    query = request.args.get('query')
    con = sqlite3.connect('instabase.db')
    cur = con.cursor()

    res = find_in_db(query, cur)
    if res == []:
        return render_template('nothing.html')
    else:
        results = []
        for i in range(len(res)):
            results.append((i+1, res[i][1], res[i][0] ))
        return render_template('results.html', results = results)

if __name__ == '__main__':
    app.run(debug=True)
