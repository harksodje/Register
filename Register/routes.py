from Register import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from Register.models import user_data
from flask import request, jsonify , make_response
import jwt
from datetime import datetime, timedelta
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        
        token = None
        if 'x-access' in request.headers:
            token = request.headers['x-access']
        if not token:
            return jsonify({'message': token is missing}), 401
        try:
            token = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = user.data.query.filter_by(id = data['id']).first()
        except:
            return jsonify({'message': 'invalid token'}), 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/user', methods = ['POST'])
@token_required
def new_user(current_user):
    # to get json data from the new user
    #if not current_user.admin :
    #return jsonify ({'message':'Unauthorize access'})#
    data = request.get_json()

    hash_password = generate_password_hash(data['password'], method= 'sha256' )
    user = user_data(username = data['username'], email = data['email'], password = hash_password)

    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'new user created'})
    #return jsonify({'message': ' no details filled!'})
@app.route('/user/<id>', methods = ['POST'])
def get_user_data(id):
    user = user_data.query.filter_by(id = id)
    output = []
    for i in user:
        user = {}
        user['username'] = i.username
        user['email'] = i.email
        user['password'] =i.password
        output.append(user)
    if output: 
        return jsonify ({'user':output})
    else:
        return jsonify({'message': 'no user details'})

@app.route('/user', methods = ['GET', 'POST'])
def get_all_users():
    #auth = request.authorization
    #if auth and auth.username == 'Admin 'and auth.password =='Admin':
    users = user_data.query.all()
    output = []
    for user in users:
        user_dict = {}
        
        user_dict['username'] = user.username
        user_dict['email'] = user.email
        user_dict['admin'] = user.admin
        user_dict['password'] =user.password
        output.append(user_dict)
    return jsonify ({'user':output})
   #return jsonify({'message': 'Unauthorize login details'})

@app.route('/user/<id>', methods = ['PUT'])
def update_user(id):
    user = user_data.query.filter_by(id = id).first()
    #hint dont forget to change the id recommendation
    if int(user.id) >= 2: 
        user.admin = True
        db.session.commit()
        return jsonify({'message': "user update to admin"})
    return jsonify({'message' :' id not allow'})

@app.route('/user/<id>', methods = ['DELETE'])
def delete_user(id):
    user = user_data.query.filter_by(id = id).first()
    if user.id: 
        db.session.delete(user)
        db.session.commit() 
        return jsonify({'message': "user delete from database"})
    return jsonify({'message' :' no user data'})


@app.route('/login')
def login():
    auth = request.authorization
    if not auth and not  auth.password and not auth.username:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm = "login required !"'})
    
    user = user_data.query.filter_by(username = auth.username).first()
    if  not user :
        return jsonify ({'message': 'user not in the database'})
        
    if check_password_hash (user.password, auth.password):
        token = jwt.encode({'id': user.id, 'exp' : datetime.utcnow() + timedelta(minutes = 30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm = "login required !"'})
    