import csv

def populateFact(db, Fact):
    pass

def populateTopics(db, Topics):
    objs = []
    with open('./app/csvs/topic_id.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            objs.append({'topicId': ele[0], 'topicName': ele[1]})
        db.engine.execute(Topics.__table__.insert(), objs)

def populateFreqItems(db, FreqItems):
    objs = []
    with open('./app/csvs/freq_item_id.csv', 'r') as fl:
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
    with open('./app/csvs/author_id.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            objs.append({'authorId': ele[1], 'authorName': ele[0]})
        db.engine.execute(Author.__table__.insert(), objs)

def populatePublication(db, Publication):
    objs = []
    with open('./app/csvs/publish_dim_table.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            objs.append({'fileId': ele[0], 'date': ele[1]})
        db.engine.execute(Publication.__table__.insert(), objs)