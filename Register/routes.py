from Register import app, db
from werkzeug.security import check_password_hash, generate_password_hash
from Register.models import user_data
from flask import request, jsonify 


@app.route('/user', methods = ['POST'])
def new_user():
    # to get json data from the new user
    data = request.get_json()

    hash_password = generate_password_hash(data['password'], method= 'sha256' )
    user = user_data(username = data['username'], email = data['email'], password = data['password'])

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

@app.route('/user', methods = ['GET'])
def get_all_users():
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

@app.route('/user/<id>', methods = ['PUT'])
def update_user(id):
    user = user_data.query.filter_by(id = id).first()
    if int(user.id) <= 2: 
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
