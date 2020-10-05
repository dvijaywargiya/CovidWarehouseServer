from . import app, db
import json
from flask import request, abort, render_template
from werkzeug.utils import secure_filename
from .models import *
from uuid import uuid4
from sqlalchemy import text
import datetime
import os

# lastUploadedQuery = text('select * from uploads order by fileId desc limit 1')
# lastUploadedResult = db.engine.execute(lastUploadedQuery)

# temp = None
# for row in lastUploadedResult:
#     temp = row
#     break

# app.logger.error(temp)        
# if temp == None:
#     lastUploadedId = 0
# else:
#     lastUploadedId = temp.fileId

# lastUploadedId = int(lastUploadedId)

@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template("index.html", flask_token="Hello World")

@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template("index.html", flask_token="Hello World")

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template("index.html", flask_token="Hello World")

@app.route('/api/uploadFile', methods=['POST'])
def fileUpload():
    file = request.files['file'] 
    filename = secure_filename(file.filename)
    global lastUploadedId
    destination="/".join([app.config['UPLOAD_FOLDER'], str(lastUploadedId)+'.pdf'])
    file.save(destination)
    response="Uploaded"
    return response

@app.route('/api/uploadedFileData', methods=['POST'])
def uploadedFileData():
    title = request.json.get('title')
    link = request.json.get('link')
    global lastUploadedId
    lastUploadedId = lastUploadedId + 1
    newUpload = Uploads(fileId=lastUploadedId, timeStamp=datetime.datetime.now(), ip='', title=title, link=link)
    db.session.add(newUpload)
    db.session.commit()
    return "Success"

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

@app.route('/api/getLocations', methods=['GET'])
def getLocations():
    locations = Location.query.all() 
    ret = []
    for ele in locations:
        ret.append({'locationId': ele.locationId, 'locationName': ele.locationName})
    return json.dumps(ret)


def intersection(lst1, lst2): 
    return [item for item in lst1 if item in lst2] 

def union(lst1, lst2): 
    lst = [item for item in lst1 if item in lst2 or item in lst1]
    t = []
    for ele in lst:
        if ele not in t:
            t.append(ele)
    return  t

@app.route('/api/query', methods=['POST'])
def query():
    authors = list(request.json.get('authors'))
    topics = list(request.json.get('topics'))
    locations = list(request.json.get('locations'))
    fromDate = request.json.get('fromDate')
    toDate = request.json.get('toDate')

    authorAcross = request.json.get('authorAcross')
    dateAcross = request.json.get('dateAcross')
    topicsAcross = request.json.get('topicsAcross')
    locationsAcross = request.json.get('locationsAcross')

    authors = tuple(authors)
    topics = tuple(topics)
    locations = tuple(locations)

    lists = []
    masterQuery = text('select distinct metaID from file_dimension;')
    masterResult = db.engine.execute(masterQuery)
    masterFilenames = [row[0] for row in masterResult]

    if len(authors) > 0:
        authorsQuery = None
        if len(authors) > 1:
            authorsQuery = text('select distinct metaID from authors_dimension where authorId IN {} ;'.format(authors))
        else:
            authorsQuery = text('select distinct metaID from authors_dimension where authorId = {} ;'.format(authors[0]))

        authorsResult = db.engine.execute(authorsQuery)
        authorsFilenames = [row[0] for row in authorsResult]        
        lists.append([authorsFilenames, authorAcross])
    else:
        authorsQuery = text('select distinct metaID from authors_dimension;')
        authorsResult = db.engine.execute(authorsQuery)
        authorsFilenames = [row[0] for row in authorsResult]
        
        lists.append([authorsFilenames, authorAcross])

    if len(topics) > 0:
        topicsQuery = None
        if len(topics) > 1:
            topicsQuery = text('select distinct metaID from topics_dimension where topicId IN {} ;'.format(topics))
        else:
            topicsQuery = text('select distinct metaID from topics_dimension where topicId = {} ;'.format(topics[0]))

        topicsResult = db.engine.execute(topicsQuery)
        topicsFilenames = [row[0] for row in topicsResult]
        lists.append([topicsFilenames, topicsAcross])
    else:
        topicsQuery = text('select distinct metaID from topics_dimension;')
        topicsResult = db.engine.execute(topicsQuery)
        topicsFilenames = [row[0] for row in topicsResult]
        lists.append([topicsFilenames, topicsAcross])

    if len(locations) > 0:
        locationsQuery = None
        if len(locations) > 1:
            locationsQuery = text('select distinct metaID from location_dimension where locationId IN {} ;'.format(locations))
        else:
            locationsQuery = text('select distinct metaID from location_dimension where locationId = {} ;'.format(locations[0]))

        locationsResult = db.engine.execute(locationsQuery)
        locationsFilenames = [row[0] for row in locationsResult]
        lists.append([locationsFilenames, locationsAcross])
    else:
        locationsQuery = text('select distinct metaID from location_dimension;')
        locationsResult = db.engine.execute(locationsQuery)
        locationsFilenames = [row[0] for row in locationsResult]
        lists.append([locationsFilenames, locationsAcross])

    if fromDate and toDate:
        fromDate = fromDate.split('-')
        formattedFromDate = datetime.date(int(fromDate[0]), int(fromDate[1]), int(fromDate[2]))
        toDate = toDate.split('-')
        formattedToDate = datetime.date(int(toDate[0]), int(toDate[1]), int(toDate[2]))

        try:
            dateQuery = text('select distinct metaID from publication where timestamp between "{}" and "{}";'.format(formattedFromDate, formattedToDate))
            dateResult = db.engine.execute(dateQuery)
            dateFilenames = [row[0] for row in dateResult]
            lists.append([dateFilenames, dateAcross])
        except:
            pass
    else:
        dateQuery = text('select distinct metaID from publication;')
        dateResult = db.engine.execute(dateQuery)
        dateFilenames = [row[0] for row in dateResult]
        lists.append([dateFilenames, dateAcross])

    files = masterFilenames
    for i in range(0, len(lists)):
        if lists[i][1] == "OR":
            files = union(files, lists[i][0])
        else:
            files = intersection(files, lists[i][0])

    list_to_be_returned = []
    for ele in files:
        fileQuery = text('select title, link, abstract, abstractLink from file_dimension where metaID = {} ;'.format(ele))
        fileResult = db.engine.execute(fileQuery)
        fileResult = [row for row in fileResult][0]
        list_to_be_returned.append({'title':fileResult[0],'link':fileResult[1],'abstract':fileResult[2], 'abstractLink':fileResult[3]})

    return json.dumps(list_to_be_returned)
