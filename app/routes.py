from app import app, db
import json
from flask import request, abort
from app.models import User, Author
from uuid import uuid4

@app.route('/register', methods=['POST'])
def newUser():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    try:
        newUser = User(name=name, email=email, token=str(uuid4()))
        newUser.set_password(password)
        db.session.add(newUser)
        db.session.commit()
        return json.dumps({'user': newUser.name, 'token': newUser.token})
    except:
        abort(400)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        abort(400)
    return json.dumps({'user': user.name, 'token':user.token})

@app.route('/getAuthors', methods=['GET'])
def getAuthors():
    authors = Author.query.all() 
    ret = []
    for ele in authors:
        ret.append({'authorId': ele.authorId, 'authorName': ele.authorName})
    return json.dumps(ret)