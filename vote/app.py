from flask import Flask, render_template, request, make_response, g
from redis import Redis
import os
import socket
import random
import json
import time

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
hostname = socket.gethostname()

app = Flask(__name__)

red = None

def get_redis():
    # if not hasattr(g, 'redis'):
    #     app.logger.debug("Create redis connection")
    #     g.redis = Redis(host="redis", db=0, socket_timeout=5)
    # app.logger.debug(hasattr(g, 'redis'))
    # return g.redis
    if not hasattr(app, 'redis'):
        app.redis = Redis(host="redis", db=0, socket_timeout=5)
    return app.redis

@app.route("/", methods=['POST','GET'])
def hello():

    vote = None

    if request.method == 'POST':
        voter_id = request.cookies.get('voter_id')
        redis = get_redis()
        vote = request.form['vote']
        data = json.dumps({'voter_id': voter_id, 'vote': vote})
        redis.rpush('votes', data)
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


@app.route('/' + option_a, methods=['POST'])
def option_a_vote():
    voter_id = hex(random.getrandbits(64))[2:-1]
    redis = get_redis()
    data = json.dumps({'voter_id': voter_id, 'vote': 'a'})
    redis.rpush('votes', data)
    return '', 201


@app.route('/' + option_b, methods=['POST'])
def option_b_vote():
    voter_id = hex(random.getrandbits(64))[2:-1]
    redis = get_redis()
    data = json.dumps({'voter_id': voter_id, 'vote': 'b'})
    redis.rpush('votes', data)
    return '', 201


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)
