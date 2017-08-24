from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from flask import request, jsonify
from app.models import User, Bucketlist
import jwt
import datetime
from app import config
from functools import wraps
from flask_login import current_user

@app.route('/auth/home')
def welcome():
    return "Welcome to FlaskApi"


def token_required(k):
    @wraps(k)
    def decorated(*args, **kwargs):
        token = None
        if 'user_token' in request.headers:
            token = request.headers['user_token']

        if not token:
            res = {"msg":"Token is missing"}
            return jsonify(res)
        try:
            token_decode = jwt.decode(token, app.config['SECRET'])
            current_user = User.query.filter_by(name=token_decode['name']).first()

        except:
            return jsonify({"msg": "Token is invalid"})
        return k(current_user *args, **kwargs)

    return decorated

        

@app.route('/auth/register', methods=['POST'])
def register_user():
    name = request.form.get('name')
    email = request.form.get('email')
    password = generate_password_hash(request.form.get('password'), method='sha256')
    if not name or not password:
        res = {"msg": "Please provide all the credentials"}
        return jsonify(res)
    else:
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        res = {"msg": "User added successfully"}
        return jsonify(res)


@app.route('/auth/login', methods=['POST'])
def login():
    name = request.form.get('name')
    password = request.form.get('password')
    if not name or not password:
        res = {"msg": "Please provide all the credentials"}
        return jsonify(res)
    else:
        user = User.query.filter_by(name=name).first()
        if not user:
            res = {"msg": "User not available"}
            return jsonify(res)
            
        if check_password_hash(user.password, password):
             token = jwt.encode({'name':name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET'])
             return jsonify({'token': token.decode('UTF-8')}), 202

@token_required
@app.route('/bucketlist', methods=['POST'])
def create_bucketlist():
    name = request.form.get('name')
    if not name :
        res = {"msg": "Please provide the bucketlistname"}
        return jsonify(res)
    else:
        bucketlist = Bucketlist(name=name)
        db.session.add(bucketlist)
        db.session.commit()
        res = {"msg": "bucketlist added successfully"}
        return jsonify(res)
    





    
            
        
    
   
     