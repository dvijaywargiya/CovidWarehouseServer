import csv
import datetime
from sqlalchemy import text

def populateType(db, Type):
    objs = []
    with open('./csvs/type_id.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            typeId = ele[1]
            typeName = ele[0]
            checkQuery = text('select * from type where typeId = {} ;'.format(typeId))
            checkResult = db.engine.execute(checkQuery)
            content = [row[0] for row in checkResult]
            if len(content) == 0:
                db.engine.execute(Type.__table__.insert(), typeId=typeId, typeName=typeName)

def populateTypeDimension(db, TypeDimension):
    objs = []
    with open('./csvs/type_dim_table.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            defId = ele[0]
            metaID = ele[1]
            typeId = ele[2]
            checkQuery = text('select * from type_dimension where metaID = {} ;'.format(metaID))
            checkResult = db.engine.execute(checkQuery)
            content = [row[0] for row in checkResult]
            if len(content) == 0:
                db.engine.execute(TypeDimension.__table__.insert(), id=defId, metaID=metaID, tpyeId=typeId)

def populateCategory(db, Category):
    objs = []
    with open('./csvs/category_id.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            categoryId = ele[0]
            categoryName = ele[1]
            checkQuery = text('select * from category where categoryId = {} ;'.format(categoryId))
            checkResult = db.engine.execute(checkQuery)
            content = [row[0] for row in checkResult]
            if len(content) == 0:
                db.engine.execute(Category.__table__.insert(), categoryId=categoryId, categoryName=categoryName)

def populateCategoryDimension(db, CategoryDimension):
    objs = []
    with open('./csvs/category_dim_table.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            defId = ele[0]
            metaID = ele[1]
            categoryId = ele[2]
            checkQuery = text('select * from category_dimension where metaID = {} ;'.format(metaID))
            checkResult = db.engine.execute(checkQuery)
            content = [row[0] for row in checkResult]
            if len(content) == 0:
                db.engine.execute(CategoryDimension.__table__.insert(), id = defId, metaID=metaId, categoryId=categoryId)

def populateLocation(db, Locations):
    objs = []
    with open('./csvs/location_id.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            locationId = ele[1]
            locationName = ele[0]
            checkQuery = text('select * from location where locationId = {} ;'.format(locationId))
            checkResult = db.engine.execute(checkQuery)
            content = [row[0] for row in checkResult]
            if len(content) == 0:
                db.engine.execute(Locations.__table__.insert(), locationId=locationId, locationName=locationName)
   
def populateLocationsDimension(db, LocationsDimension):
    objs = []
    with open('./csvs/location_dim_table.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            defId = ele[0]
            locationId = ele[2]
            metaID = ele[1]
            checkQuery = text('select * from location_dimension where metaID = {} ;'.format(metaID))
            checkResult = db.engine.execute(checkQuery)
            content = [row[0] for row in checkResult]
            if len(content) == 0:
                db.engine.execute(LocationDimension.__table__.insert(), id = defId, locationId=locationId, metaID=metaID)

def populateAuthorDimension(db, AuthorDimension):
    objs = []
    with open('./csvs/author_dim_table.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            defId = ele[0]
            authorId = ele[2]
            metaID = ele[1]
            checkQuery = text('select * from authors_dimension where metaID = {} ;'.format(metaID))
            checkResult = db.engine.execute(checkQuery)
            content = [row[0] for row in checkResult]
            if len(content) == 0:
                db.engine.execute(AuthorDimension.__table__.insert(), id = defId, authorId=authorId, metaID=metaID)

def populateTopicsDimension(db, TopicsDimension):
    objs = []
    with open('./csvs/topics_dim_table.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            objs.append({'id': val, 'topicId': ele[1], 'metaID': ele[0]})
            defId = ele[0]
            topicId = ele[2]
            metaID = ele[1]
            checkQuery = text('select * from topics_dimension where metaID = {} ;'.format(metaID))
            checkResult = db.engine.execute(checkQuery)
            content = [row[0] for row in checkResult]
            if len(content) == 0:
                db.engine.execute(TopicsDimension.__table__.insert(), id = defId, topicId=authorId, metaID=metaID)

def populateTopics(db, Topics):
    objs = []
    with open('./csvs/topic_id.csv', 'r') as fl:
        reader = csv.reader(fl)
        for ele in reader:
            objs.append({'topicId': ele[0], 'topicName': ele[1]})
        db.engine.execute(Topics.__table__.insert(), objs)

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
