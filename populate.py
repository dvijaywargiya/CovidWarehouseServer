import csv
import datetime

def populateType(db, Type):
    objs = []
    with open('./csvs/type_id.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            objs.append({'typeId': ele[1], 'typeName': ele[0]})
        db.engine.execute(Type.__table__.insert(), objs)


def populateTypeDimension(db, TypeDimension):
    objs = []
    with open('./csvs/type_dim_table.csv', 'r') as fl:
        reader = csv.reader(fl)
        val = 1
        for ele in reader:
            objs.append({'id': val, 'typeId': ele[1], 'metaID': ele[0]})
            val = val + 1
        db.engine.execute(TypeDimension.__table__.insert(), objs)

def populateLocation(db, Locations):
    objs = []
    with open('./csvs/location_id.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            objs.append({'locationId': ele[1], 'locationName': ele[0]})
        db.engine.execute(Locations.__table__.insert(), objs)

def populateLocationsDimension(db, LocationsDimension):
    objs = []
    with open('./csvs/location_dim_table.csv', 'r') as fl:
        reader = csv.reader(fl)
        val = 1
        for ele in reader:
            objs.append({'id': val, 'locationId': ele[1], 'metaID': ele[0]})
            val = val + 1
        db.engine.execute(LocationsDimension.__table__.insert(), objs)


def populateAuthorDimension(db, AuthorDimension):
    objs = []
    with open('./csvs/author_dim_table.csv', 'r') as fl:
        reader = csv.reader(fl)
        val = 1
        for ele in reader:
            objs.append({'id': val, 'authorId': ele[1], 'metaID': ele[0]})
            val = val + 1
        db.engine.execute(AuthorDimension.__table__.insert(), objs)

def populateTopicsDimension(db, TopicsDimension):
    objs = []
    with open('./csvs/topics_dim_table.csv', 'r') as fl:
        reader = csv.reader(fl)
        val = 1
        for ele in reader:
            objs.append({'id': val, 'topicId': ele[1], 'metaID': ele[0]})
            val = val + 1
        db.engine.execute(TopicsDimension.__table__.insert(), objs)

def populateTopics(db, Topics):
    objs = []
    with open('./csvs/topic_id.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            objs.append({'topicId': ele[0], 'topicName': ele[1]})
        db.engine.execute(Topics.__table__.insert(), objs)

def populateFreqItems(db, FreqItems):
    objs = []
    with open('./csvs/freq_item_id.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            id = ele[-1]
            del ele[-1]
            ele = ','.join(ele)
            ele = ele.strip('[')
            ele = ele.strip(']')
            objs.append({'itemSetId': id, 'itemSet': ele})
        db.engine.execute(FreqItems.__table__.insert(), objs)

def populateAuthor(db, Author):
    objs = []
    with open('./csvs/author_id.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            objs.append({'authorId': ele[1], 'authorName': ele[0]})
        db.engine.execute(Author.__table__.insert(), objs)

def populatePublication(db, Publication):
    objs = []
    with open('./csvs/publish_dim_table.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            temp = ele[1].split(' ')[0].split('-')
            timestamp = datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))
            objs.append({'metaID': ele[0], 'timestamp': timestamp})
        db.engine.execute(Publication.__table__.insert(), objs)

def populateFileDimension(db, FileDimension):
    objs = []
    with open('./csvs/fact_display.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            objs.append({'metaID': ele[0], 'fileName': ele[1], 'title':ele[2], 'link':ele[3], 'abstract':ele[4], 'abstractLink': ele[5]})
        db.engine.execute(FileDimension.__table__.insert(), objs)
