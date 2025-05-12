from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from models.user_model import User, Session
from flask_cors import CORS, cross_origin

app = Flask(__name__)
session = Session()
CORS(app, resources={r"*": {"origins": "*"}})

def user_exists(username):
    user = session.query(User).filter_by(username=username).first()
    return user

def create_test_user():
    if session.query(User).filter_by(username="test").first() is None:
        hashed = generate_password_hash("test")
        new_user = User(username="test", password=hashed)
        session.add(new_user)
        session.commit()
    print("Test user was created!")

create_test_user()
    
@cross_origin
@app.route("/api/login",  methods=['POST'])
def login():
    data = request.get_json() 

    username = data.get("username")
    password = data.get("password")

    user = user_exists(username)

    if not user:
        return jsonify({"message" : "User was not found"}), 404
    
    if check_password_hash(user.password, password):
        return jsonify({"message": "Login successful"}), 200
    
    else:
        return jsonify({"message" : "Incorrect password"}), 401

if __name__ == "__main__":
	Flask.run(app, host="127.0.0.1", port=5000)   

    
    