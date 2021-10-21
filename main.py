from flask import Flask
from flask import render_template, request


from search_func import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('search.html')

@app.route('/how_to', methods = ['GET'])
def how_to():
        return render_template('how_to.html')

@app.route('/results', methods = ['GET'])
def results():
    query = request.args.get('query')


    res = find_in_db(query)
    if res == []:
        return render_template('nothing.html')
    else:
        results = []
        for i in range(len(res)):
            results.append((i+1, res[i][1], res[i][0] ))
        return render_template('results.html', results = results)

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
