from app import app, db
import json
from flask import request, abort
from app.models import User, Author, Topics, AuthorsDimension, TopicsDimension
from uuid import uuid4
from sqlalchemy import text

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

@app.route('/getTopics', methods=['GET'])
def getTopics():
    topics = Topics.query.all() 
    ret = []
    for ele in topics:
        ret.append({'topicId': ele.topicId, 'topicName': ele.topicName})
    return json.dumps(ret)

@app.route('/query', methods=['POST'])
def query():
    authors = list(request.json.get('authors'))
    topics = list(request.json.get('topics'))
    authors = tuple(authors)
    topics = tuple(topics)

    if len(authors) > 0:
        authorsQuery = None
        if len(authors) > 1:
            authorsQuery = text('select fileName from authors_dimension where authorId IN {} ;'.format(authors))
        else:
            authorsQuery = text('select fileName from authors_dimension where authorId = {} ;'.format(authors[0]))

        authorsResult = db.engine.execute(authorsQuery)
        authorsFilenames = [row[0] for row in authorsResult]

    if len(topics) > 0:
        topicsQuery = None
        if len(topics) > 1:
            topicsQuery = text('select fileName from topics_dimension where topicId IN {} ;'.format(topics))
        else:
            topicsQuery = text('select fileName from topics_dimension where topicId = {} ;'.format(topics[0]))

        topicsResult = db.engine.execute(topicsQuery)
        topicsFilenames = [row[0] for row in topicsResult]

    files = list(set(topicsResult) & set(authorsResult)) 

    return json.dumps(files)
