from flask import Flask, render_template, request, make_response, g, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from redis import Redis
import os
import socket
import random
import json

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres@db/postgres'
db = SQLAlchemy(app)


def get_responses():
    a_res, b_res = (0, 0)
    try:
        db.engine.execute('CREATE TABLE IF NOT EXISTS votes (id VARCHAR(255) NOT NULL UNIQUE, vote VARCHAR(255) NOT NULL)')
        res = db.engine.execute('SELECT vote, COUNT(id) AS count FROM votes GROUP BY vote')
        for result in res:
            if result[0] == 'a':
                a_res = result[1]
            else:
                b_res = result[1]
    except:
        pass
    return a_res, b_res


@app.route("/", methods=['POST','GET'])
def hello():

    vote = None

    if request.method == 'POST':
        voter_id = request.cookies.get('voter_id')
        vote = request.form['vote']
        try:
            db.engine.execute("INSERT INTO votes (id, vote) VALUES ('{}', '{}')".format(voter_id, vote))
        except :
            db.engine.execute("UPDATE votes SET vote = '{}' where id = '{}'".format(vote, voter_id))
    else:
        voter_id = hex(random.getrandbits(64))[2:-1]

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))
    resp.set_cookie('voter_id', voter_id)
    return resp


@app.route("/results/", methods=['GET'])
def results():
    a_res, b_res = get_responses()
    if a_res + b_res != 0:
        option_a_res = int(a_res / float(a_res + b_res) * 100)
        option_b_res = int(b_res / float(a_res + b_res) * 100)
    else:
        option_a_res = 50
        option_b_res = 50

    resp = make_response(render_template(
        'results.html',
        hostname=hostname,
        option_a_res=option_a_res,
        option_b_res=option_b_res,
        total=a_res + b_res,
    ))
    return resp


@app.route("/poll/", methods=['GET'])
def poll():
    a_res, b_res = get_responses()
    if a_res + b_res != 0:
        option_a_res = int(a_res / float(a_res + b_res) * 100)
        option_b_res = int(b_res / float(a_res + b_res) * 100)
    else:
        option_a_res = 50
        option_b_res = 50
    return jsonify(
        option_a_res=option_a_res,
        option_b_res=option_b_res,
        total=a_res + b_res,
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
