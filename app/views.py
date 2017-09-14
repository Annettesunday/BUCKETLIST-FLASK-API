from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from flask import request, jsonify
from app.models import User, Bucketlist, BucketlistItem
import jwt
import datetime
from app import config
from functools import wraps
from flask_login import current_user, UserMixin

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
        return k(current_user, *args, **kwargs)

    return decorated

        

@app.route('/auth/register', methods=['POST'])
def register_user():
    """Registers new users"""
    user = request.get_json()
    name = request.json.get('name')
    email = request.json.get('email')
    password = generate_password_hash(request.json.get('password'), method='sha256')
    if 'name' and 'password' and 'email' not in user:
        res = {"msg": "Please provide all the credentials"}, 400
        return jsonify(res)
    else:
        user = User.query.filter_by(name=name).first()
        if user:
            res = {"error": "User name already exists.Try again with a different name"}, 400
            return jsonify(res)

        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "User added successfully"}), 201


@app.route('/auth/login', methods=['POST'])
def login():
    """logs in registered users"""
    name = request.json.get('name')
    password = request.json.get('password')
    #prevents login without user name and password
    if not name or not password:
        res = {"msg": "Please provide all the credentials"}
        return jsonify(res)
    else:
        #fetch user records from db
        user = User.query.filter_by(name=name).first()
        if not user:
            res = {"msg": "User not available"}
            return jsonify(res)
          #generate token  
        if check_password_hash(user.password, password):
             token = jwt.encode({'name':name, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET'])
             return jsonify({'token': token.decode('UTF-8')}), 202
        else:
            return jsonify({"msg": "wrong password"})

@app.route('/bucketlist', methods=['POST'])
@token_required
def create_bucketlist(current_user):
    name = request.json.get('name')
    if not name :
        res = {"msg": "Please provide the bucketlistname"}
        return jsonify(res)
    else:
        bucketlist = Bucketlist(name=name, owner_id=current_user.id)
        db.session.add(bucketlist)
        db.session.commit()
        res = {"msg": "bucketlist added successfully"}
        return jsonify(res)
    

@app.route('/bucketlist/<bucketlistID>', methods=['DELETE'])
@token_required
def delete_bucketlist(current_user, bucketlistID):
    name = Bucketlist.query.filter_by(id=bucketlistID, owner_id=current_user.id).first()
    if not name:
        res = {"msg": "Bucketlist not found"}
        return jsonify(res)
    else:
        db.session.delete(name)
        db.session.commit()
        res = {"msg": "You have deleted a bucketlist successfully"}
        return jsonify(res)

@app.route('/bucketlist/<bucketlistID>', methods=['PUT'])
@token_required
def edit_bucketlist(current_user, bucketlistID):
    newname = request.json.get('newname')
    name = Bucketlist.query.filter_by(id=bucketlistID, owner_id=current_user.id).first()
    if not name:
        res = {"msg": "Bucketlist not found"}
        return jsonify(res)
    else:
        name.name = newname
        db.session.commit()
        res = {"msg": "Bucketlistname has been updated"}
        return jsonify(res), 200

@app.route('/bucketlist/<bucketlistID>', methods=['GET'])
@token_required
def get_bucketlist(current_user, bucketlistID):
    name = Bucketlist.query.filter_by(id=bucketlistID, owner_id=current_user.id).first()
    if not name:
        res = {"msg": "Bucketlist not found"}
        return jsonify(res)
    else:
        bucketlist_dict = {}
        bucketlist_dict['owner_id'] = name.owner_id
        bucketlist_dict['bucketlist_id'] = name.id
        bucketlist_dict['name'] = name.name
        return jsonify(bucketlist_dict)

@app.route('/bucketlist/', methods=['GET'])
@token_required
def get_all_bucketlists(current_user):
    search = request.args.get("q")
    if search:
        bucketlist = Bucketlist.query.filter_by(owner_id=current_user.id, name=search).first()

        if bucketlist:
            allbucketlists_dict = {}
            allbucketlists_dict['owner_id'] = bucketlist.owner_id
            allbucketlists_dict['name'] = bucketlist.name
            allbucketlists_dict['bucketlist_id'] = bucketlist.id
            return jsonify(allbucketlists_dict)
        return jsonify("Bucketlist not found")
    url = "/bucketlist/"
    
    limit = request.args.get("limit")       
    if limit and int(limit) < 10:
        limit = int(request.args.get("limit"))
    else:
        limit = 10

    if request.args.get("page"):
        page = int(request.args.get("page"))
    else:
        page = 1
    bucketlist = Bucketlist.query.filter_by(owner_id=current_user.id).paginate(page, limit, False)

    if bucketlist.has_next:
        next_page = url + '?page=' + str(page + 1) + '&limit=' + str(limit)
    else:
        next_page = ""
    if bucketlist.has_next:
        next_page = url + '?page=' + str(page - 1) + '&limit=' + str(limit)
    else:
        previous_page = ""

    

    names = Bucketlist.query.filter_by(owner_id=current_user.id).all()
    bucket_list =[]
    for name in  names:
        allbucketlists_dict = {}
        allbucketlists_dict['owner_id'] = name.owner_id
        allbucketlists_dict['name'] = name.name
        allbucketlists_dict['bucketlist_id'] = name.id
        bucket_list.append(allbucketlists_dict)
    print(bucket_list)    
    return jsonify(bucket_list)

@app.route('/bucketlist/<bucketlistID>/items', methods=['POST'])
@token_required
def add_item(current_user, bucketlistID):
    description = request.json.get('description')
    if not description :
        res = {"msg": "Please provide the itemname"}
        return jsonify(res)
    else:
        description = BucketlistItem(description=description, bucketlist_id=bucketlistID)
        db.session.add(description)
        db.session.commit()
        res = {"msg": "bucketlistitem added successfully"}
        return jsonify(res)

@app.route('/bucketlist/<bucketlistID>/items/<itemID>', methods=['DELETE'])
@token_required
def delete_item(current_user, bucketlistID, itemID):
    description = BucketlistItem.query.filter_by(id=itemID, bucketlist_id=bucketlistID).first()
    if not description:
        res = {"msg": "Bucketlistitem not found"}
        return jsonify(res)
    else:
        db.session.delete(description)
        db.session.commit()
        res = {"msg": "You have deleted a bucketlistitem successfully"}
        return jsonify(res)


@app.route('/bucketlist/<bucketlistID>/items/<itemID>', methods=['PUT'])
@token_required
def edit_item(current_user, bucketlistID, itemID):
    newname = request.json.get('newname')
    description = BucketlistItem.query.filter_by(id=itemID, bucketlist_id=bucketlistID).first()
    if not description:
        res = {"msg": "BucketlistItem not found"}
        return jsonify(res)
    else:
        description.description = newname
        db.session.commit()
        res = {"msg": "Bucketlistitem has been updated"}
        return jsonify(res), 200

























