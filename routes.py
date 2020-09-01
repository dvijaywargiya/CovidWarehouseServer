from . import app, db
import json
from flask import request, abort, render_template
from .models import User, Author, Topics, AuthorsDimension, TopicsDimension, Fact
from uuid import uuid4
from sqlalchemy import text

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template("index.html", flask_token="Hello World")

@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template("index.html", flask_token="Hello World")

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("index.html", flask_token="Hello World")

@app.route('/api/register', methods=['POST'])
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

@app.route('/api/authenticate', methods=['POST'])
def authenticate():
    email = request.json.get('email')
    password = request.json.get('password')
    user = User.query.filter_by(email=email).first()
    if user is None or not user.check_password(password):
        abort(400)
    return json.dumps({'user': user.name, 'token':user.token})

@app.route('/api/getAuthors', methods=['GET'])
def getAuthors():
    authors = Author.query.all() 
    ret = []
    for ele in authors:
        ret.append({'authorId': ele.authorId, 'authorName': ele.authorName})
    return json.dumps(ret)

@app.route('/api/getTopics', methods=['GET'])
def getTopics():
    topics = Topics.query.all() 
    ret = []
    for ele in topics:
        ret.append({'topicId': ele.topicId, 'topicName': ele.topicName})
    return json.dumps(ret)

def intersection(lst1, lst2): 
    return [item for item in lst1 if item in lst2] 

@app.route('/api/query', methods=['POST'])
def query():
    authors = list(request.json.get('authors'))
    topics = list(request.json.get('topics'))
    fromYear = request.json.get('fromYear')
    toYear = request.json.get('toYear')
    authors = tuple(authors)
    topics = tuple(topics)

    lists = []
    if len(authors) > 0:
        authorsQuery = None
        if len(authors) > 1:
            authorsQuery = text('select distinct metaID from authors_dimension where authorId IN {} ;'.format(authors))
        else:
            authorsQuery = text('select distinct metaID from authors_dimension where authorId = {} ;'.format(authors[0]))

        authorsResult = db.engine.execute(authorsQuery)
        authorsFilenames = [row[0] for row in authorsResult]
        app.logger.error("--------")
        app.logger.error(authorsFilenames)
        app.logger.error("--------")
        if len(authorsFilenames) > 0:
            lists.append(authorsFilenames)
    else:
        authorsQuery = text('select distinct metaID from authors_dimension;')
        authorsResult = db.engine.execute(authorsQuery)
        authorsFilenames = [row[0] for row in authorsResult]
        if len(authorsFilenames) > 0:
            lists.append(authorsFilenames)

    if len(topics) > 0:
        topicsQuery = None
        if len(topics) > 1:
            topicsQuery = text('select distinct metaID from topics_dimension where topicId IN {} ;'.format(topics))
        else:
            topicsQuery = text('select distinct metaID from topics_dimension where topicId = {} ;'.format(topics[0]))

        topicsResult = db.engine.execute(topicsQuery)
        topicsFilenames = [row[0] for row in topicsResult]
        if len(topicsFilenames) > 0:
            lists.append(topicsFilenames)
    else:
        topicsQuery = text('select distinct metaID from topics_dimension;')
        topicsResult = db.engine.execute(topicsQuery)
        topicsFilenames = [row[0] for row in topicsResult]
        if len(topicsFilenames) > 0:
            lists.append(topicsFilenames)


    if fromYear and toYear:
        try:
            fromYear = int(fromYear)
            toYear = int(toYear)
            dateQuery = text('select distinct metaID from publication where date between {} AND {};'.format(fromYear, toYear))
            dateResult = db.engine.execute(dateQuery)
            dateFilenames = [row[0] for row in dateResult]
            if len(dateFilenames) > 0:
                lists.append(dateFilenames)
        except:
            pass
    else:
        dateQuery = text('select distinct metaID from publication;')
        dateResult = db.engine.execute(dateQuery)
        dateFilenames = [row[0] for row in dateResult]
        if len(dateFilenames) > 0:
            lists.append(dateFilenames)

    files = lists[0]
    for i in range(1, len(lists)):
        files = intersection(files, lists[i])

    list_to_be_returned = []
    for ele in files:
        fileQuery = text('select title,link,abstract from file_dimension where metaID = {} ;'.format(ele))
        fileResult = db.engine.execute(fileQuery)
        fileResult = [row for row in fileResult][0]
        list_to_be_returned.append({'title':fileResult[0],'link':fileResult[1],'abstract':fileResult[2]})

    return json.dumps(list_to_be_returned)
