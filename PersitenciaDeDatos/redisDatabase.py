import redis
import pickle
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

user = [{"name":"Gerardo"},{"products": [{"name":"carro"}]}]

json_user = json.dumps(user)

r.set("user", json_user)

print(r.get("user"))

