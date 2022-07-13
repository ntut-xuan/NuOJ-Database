#!/usr/bin/env python3
from flask import *
import redis
import json
from database_util import test_database_connect
from problem_app import problem
from user_app import user

app = Flask(__name__)
app.register_blueprint(problem)
app.register_blueprint(user)

@app.route("/heartbeat", methods=["GET"])
def heartbeat():
    return {"status": "OK"}

if __name__ == "__main__":
    test_database_connect()
    app.run(host="0.0.0.0", port=3349)