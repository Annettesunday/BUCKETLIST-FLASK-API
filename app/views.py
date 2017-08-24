from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from flask import request, jsonify
from app.models import User
import jwt
import datetime
from app import config

@app.route('/home')
def welcome():
    return "Welcome to FlaskApi"

@app.route('/register', methods=['POST'])
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


@app.route('/login', methods=['POST'])
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


    
            
        
    
   
     