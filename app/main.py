from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from flask import Flask, jsonify, request, json
import pymongo
from bson.objectid import ObjectId
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'secret'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/api/auth/signin', methods=['POST'])
def l():
    client = pymongo.MongoClient("mongodb+srv://Ujjwal_Gupta:ujjwal@cluster0.tr3aj.mongodb.net/myDB?retryWrites=true&w=majority")
    db = client.get_database('myDB')
    records = db.users
    username = request.get_json()['username']
    password = request.get_json()['password']
    result = ""
	
    response = records.find_one({'username' : username})

    if response:	
        if bcrypt.check_password_hash(response['password'], password):
            access_token = create_access_token(identity = {
			    'username': response['username']
            })
            result = jsonify({"token":access_token})
        else:
            result = jsonify({"error":"Invalid username and password"})            
    else:
        result = jsonify({"result":"No results found"})
    return result

@app.route('/api/auth/signup', methods=['POST'])
def reg():
    client = pymongo.MongoClient("mongodb+srv://Ujjwal_Gupta:ujjwal@cluster0.tr3aj.mongodb.net/myDB?retryWrites=true&w=majority")
    db = client.get_database('myDB')
    records = db.users

    username = request.get_json()['username']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()
    print(username,email,password,created)
    user_id = records.insert_one({
	'username' : username, 
	'email' : email, 
	'password' : password, 
	'created' : created, 
	})
    # new_user = records.find_one({'_id' : user_id})
    result = {'email' : email + ' registered'}
    return jsonify({'result' : result})

@app.route('/api/total', methods=['POST'])
def t():
    client = pymongo.MongoClient("mongodb+srv://Ujjwal_Gupta:ujjwal@cluster0.tr3aj.mongodb.net/myDB?retryWrites=true&w=majority")
    db = client.get_database('myDB')
    records = db.total

    username = request.get_json()['username']
    storyname = request.get_json()['storyname']
    db.total.update({ "username": username,"storyname":storyname }, 
    { "username": username,"storyname":storyname },
     upsert=True )
    db.curr.update({ "username": username,"storyname":storyname }, 
    { "username": username,"storyname":storyname },
     upsert=True )
    number=records.count_documents({"storyname":storyname})
    numberone=db.curr.count_documents({"storyname":storyname})
    return jsonify({'total' : number,'curr':numberone})

@app.route('/api/curr', methods=['POST'])
def rdel():
    client = pymongo.MongoClient("mongodb+srv://Ujjwal_Gupta:ujjwal@cluster0.tr3aj.mongodb.net/myDB?retryWrites=true&w=majority")
    db = client.get_database('myDB')
    records = db.curr
    username = request.get_json()['username']
    storyname = request.get_json()['storyname']
    records.delete_one({ "username": username,"storyname":storyname })
    return jsonify({'result' : "done"})

@app.route('/api/counting', methods=['POST'])
def ut():
    client = pymongo.MongoClient("mongodb+srv://Ujjwal_Gupta:ujjwal@cluster0.tr3aj.mongodb.net/myDB?retryWrites=true&w=majority")
    db = client.get_database('myDB')
    records = db.total
    storyname = request.get_json()['storyname']
    number=records.count_documents({"storyname":storyname})
    numberone=db.curr.count_documents({"storyname":storyname})
    return jsonify({'total' : number,'curr':numberone})
	
	
	
if __name__ == '__main__':
    app.run(host="0.0.0.0",threaded=True,port=8080)