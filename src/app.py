from flask import Flask, request, jsonify
from pymongo import MongoClient
from functools import wraps

app = Flask(__name__)

mongodb_client = MongoClient("mongodb://localhost:27017/")
db = mongodb_client["userdb"]
users_collection = db["Users"]


# decorator for checking Authorization header
def token_required(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		if 'Authorization' in request.headers:
			token = request.headers["Authorization"]
			if token == 'Bearer B1n0FlddHVnfBLeAkC':
				return f(*args, **kwargs)
			else:
				return jsonify({'msg': 'invalid token'})
		else:
			return jsonify({'msg': 'invalid token'})
	return decorator


@app.route("/api/v1/create_user", methods=["POST"])
@token_required
def register():
	user = request.get_json()
	user_obj = users_collection.find_one({"username": user["username"]})
	if not user_obj:
		if user["username"] and user["password"] and user["age"]:
			users_collection.insert_one(user)
			return jsonify({'msg': 'User created successfully'}), 201
		else:
			return jsonify({'msg': 'field required'}), 400
	else:
		return jsonify({'msg': 'user already exist'}), 409