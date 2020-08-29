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
            authorsQuery = text('select fileName from authors_dimension where authorId IN {} ;'.format(authors))
        else:
            authorsQuery = text('select fileName from authors_dimension where authorId = {} ;'.format(authors[0]))

        authorsResult = db.engine.execute(authorsQuery)
        authorsFilenames = [row[0] for row in authorsResult]
        if len(authorsFilenames) > 0:
            lists.append(authorsFilenames)

    if len(topics) > 0:
        topicsQuery = None
        if len(topics) > 1:
            topicsQuery = text('select fileName from topics_dimension where topicId IN {} ;'.format(topics))
        else:
            topicsQuery = text('select fileName from topics_dimension where topicId = {} ;'.format(topics[0]))

        topicsResult = db.engine.execute(topicsQuery)
        topicsFilenames = [row[0] for row in topicsResult]
        if len(topicsFilenames) > 0:
            lists.append(topicsFilenames)

    if fromYear and toYear:
        try:
            fromYear = int(fromYear)
            toYear = int(toYear)
            dateQuery = text('select fileId from publication where year between {} AND {};'.format(fromYear, toYear))
            dateResult = db.engine.execute(dateQuery)
            dateFilenames = [row[0] for row in dateResult]
            if len(dateFilenames) > 0:
                lists.append(dateFilenames)
        except:
            pass

    files = lists[0]
    for i in range(1, len(lists)):
        files = intersection(files, lists[i])
   # if len(files) > 0:
    #    listToBeReturned = []
     #   for ele in files:
      #      linkQuery = text('select pdfLink, title, abstract from Fact where arxivId = {};'.format(ele))
       #     linkResult = db.engine.execute(linkQuery)
        #    app.logger.error(linkResult)
            # pdfLink = linkResult[0][0]
            # title = linkResult[0][1]
            # abstract = linkResult[0][2]
            # listToBeReturned.append([title, pdfLink, abstract])

    return json.dumps(files)
