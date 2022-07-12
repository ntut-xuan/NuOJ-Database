#!/usr/bin/env python3
from flask import *
import redis
import json

app = Flask(__name__)

def fliter_by_args(data_dict, args):
    if len(args) == 0:
        return list(data_dict.values())
    
    filter_list = []
    for key in data_dict.keys():
        data = data_dict[key]
        flag = True
        for arg_key in args.keys():
            if arg_key not in data.keys() or data[arg_key] != args[arg_key]:
                flag = False
                continue
        if flag:
            filter_list.append(data)
    return filter_list

@app.route("/users/<username>/", methods=["GET"])
def get_user(username):
    redis_app = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    user_db = json.loads(redis_app.get("user"))
    response = {"status": "OK"}
    if username not in user_db.keys():
        response = {"status": "Failed", "message": "Query username not found in database."}
        return Response(json.dumps(response), mimetype="application/json")
    user_data = user_db[username]
    response["data"] = user_data
    redis_app.close()
    return Response(json.dumps(response), mimetype="application/json")


@app.route("/users/", methods=["GET"])
def get_all_users():
    args = request.args
    response = {"status": "OK"}
    redis_app = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    user_db = json.loads(redis_app.get("user"))
    response["data"] = fliter_by_args(user_db, args)
    return Response(json.dumps(response), mimetype="application/json")

@app.route("/users/", methods=["POST"])
def create_user():

    data = request.data
    response = {"status": "OK"}
    redis_app = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    user_data = json.loads(redis_app.get("user"))
    
    if data == None:
        response = {"status": "Failed", "message": "Require body."}
        return Response(json.dumps(response), mimetype="application/json")

    json_data = json.loads(data)
    user_data[json_data["username"]] = json_data
    redis_app.set("user", json.dumps(user_data))
    redis_app.close()
    return Response(json.dumps(response), mimetype="application/json")

@app.route("/users/<username>/", methods=["PUT"])
def update_user(username):
    data = request.data
    response = {"status": "OK"}
    redis_app = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    user_db = json.loads(redis_app.get("user"))
    
    if data == None:
        response = {"status": "Failed", "message": "Require body."}
        return Response(json.dumps(response), mimetype="application/json")

    json_data = json.loads(data)
    user_data = user_db[username]
    for key in json_data.keys():
        user_data[key] = json_data[key]
    redis_app.set("user", json.dumps(user_db))
    redis_app.close()
    return Response(json.dumps(response), mimetype="application/json")

@app.route("/heartbeat", methods=["GET"])
def heartbeat():
    return {"status": "OK"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3349)