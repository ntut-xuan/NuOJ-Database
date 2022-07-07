import redis
import json

def setup_profile():
    redis_db = redis.Redis(host='localhost', port=6379, decode_responses=True)
    nuoj_user = {"nuoj": {"username": "nuoj", "password": "ff9c3cc1cd8a2cb0ffd4059a4717cdf1", "email": "NuOJ@nuoj.org.tw", "admin": 1}}
    redis_db.set("user", str(json.dumps(nuoj_user)))
    redis_db.close()

setup_profile()