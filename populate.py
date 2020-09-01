import csv

def populateAuthorDimension(db, AuthorDimension):
    objs = []
    with open('./csvs/author_dim_table.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            objs.append({'authorId': ele[1], 'metaID': ele[0]})
        db.engine.execute(AuthorDimension.__table__.insert(), objs)

def populateTopicsDimension(db, TopicsDimension):
    objs = []
    with open('./csvs/topics_dim_table.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            objs.append({'topicId': ele[1], 'metaID': ele[0]})
        db.engine.execute(TopicsDimension.__table__.insert(), objs)

def populateFact(db, Fact):
    objs = []
    with open('./csvs/Metainfo_arxiv.csv', 'r') as fl:
        reader = csv.reader(fl)
        reader.__next__()
        for ele in reader:
            authors = []
            try:
                for ele2 in ele[7].split(','):
                    authors.append(ele2.split('\'')[-2])
                authors = ','.join(authors)
            except:
                authors = []
            objs.append({'id': ele[0], 'metaId': ele[1], 'arxivId': ele[3], 'title': ele[4], 'pdfLink': ele[5], 'abstract': ele[6], 'authors': authors, 'publishedDate': ele[8]})
        db.engine.execute(Fact.__table__.insert(), objs)
                

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
            date = ele[1].split(' ')[0].split('-')[0]
            objs.append({'metaID': ele[0], 'date': date})
        db.engine.execute(Publication.__table__.insert(), objs)
