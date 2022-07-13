from database_util import fliter_by_args
from flask import *
import redis


problem = Blueprint("problem", __name__)


@problem.route("/problems/<problem_pid>/", methods=["GET"])
def get_problem(problem_pid):
    redis_app = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    problem_db = json.loads(redis_app.get("problem"))
    response = {"status": "OK"}
    if problem_pid not in problem_db.keys():
        response = {"status": "Failed", "message": "Query problem_pid not found in database."}
        return Response(json.dumps(response), mimetype="application/json")
    problem_data = problem_db[problem_pid]
    response["data"] = problem_data
    redis_app.close()
    return Response(json.dumps(response), mimetype="application/json")


@problem.route("/problems/", methods=["GET"])
def get_all_users():
    args = request.args
    response = {"status": "OK"}
    redis_app = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    problem_db = json.loads(redis_app.get("problem"))
    response["data"] = fliter_by_args(problem_db, args)
    return Response(json.dumps(response), mimetype="application/json")


@problem.route("/problems/", methods=["POST"])
def add_new_problem():
    data = request.data
    response = {"status": "OK"}
    redis_app = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    problem_db = json.loads(redis_app.get("problem"))
    
    if data == None:
        response = {"status": "Failed", "message": "Require body."}
        return Response(json.dumps(response), mimetype="application/json")

    json_data = json.loads(data)
    problem_db[json_data["problem_pid"]] = json_data
    redis_app.set("problem", json.dumps(problem_db))
    redis_app.close()
    return Response(json.dumps(response), mimetype="application/json")

@problem.route("/problems/<PID>/", methods=["PUT"])
def update_problem(PID):
    data = request.data
    response = {"status": "OK"}
    redis_app = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    problem_db = json.loads(redis_app.get("problem"))
    if data == None:
        response = {"status": "Failed", "message": "Require body."}
        return Response(json.dumps(response), mimetype="application/json")
    json_data = json.loads(data)
    problem_data = problem_db[PID]
    for key in json_data.keys():
        problem_data[key] = json_data[key]
    problem_db[PID] = problem_data
    redis_app.set("problem", json.dumps(problem_db))
    redis_app.close()
    return Response(json.dumps(response), mimetype="application/json")

@problem.route("/problems/<problem_pid>/", methods=["DELETE"])
def delete_problem(problem_pid):
    data = request.data
    response = {"status": "OK"}
    redis_app = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    problem_db = json.loads(redis_app.get("problem"))
    del problem_db[problem_pid]
    redis_app.set("problem", json.dumps(problem_db))
    redis_app.close()
    return Response(json.dumps(response), mimetype="application/json")