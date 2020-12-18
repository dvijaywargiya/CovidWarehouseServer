from sqlalchemy import text
import datetime

def masterResult(db, selectedTypes):
    masterTypeQuery = ""
    if len(selectedTypes) > 1:
        masterTypeQuery = text('select distinct metaID from type_dimension where typeId IN {} ;'.format(selectedTypes))
    else:
        masterTypeQuery = text('select distinct metaID from type_dimension where typeId = {} ;'.format(selectedTypes[0]))
    masterTypeResult = db.engine.execute(masterTypeQuery)
    masterTypeFilenames = [row[0] for row in masterTypeResult]

    masterQuery = text('select distinct metaID from file_dimension;')
    masterResult = db.engine.execute(masterQuery)
    masterFilenames = [row[0] for row in masterResult]

    return [masterFilenames, masterTypeFilenames]

def fileResults(db, files):
    if len(files) > 1:
        fileQuery = text('select title, link, abstract, abstractLink from file_dimension where metaID in {} ;'.format(files))
    else:
        fileQuery = text('select title, link, abstract, abstractLink from file_dimension where metaID = {} ;'.format(files[0]))
    fileResult = db.engine.execute(fileQuery)
    fileResult = [row for row in fileResult]
    return fileResult

def categoryResult(db, categories, categoriesAcross):
    categoryQuery = None
    if len(categories) > 1:
        categoryQuery = text('select distinct metaID from category where categoryId IN {} ;'.format(categories))
    else:
        categoryQuery = text('select distinct metaID from category where categoryId = {} ;'.format(categories[0]))

    categoriesResult = db.engine.execute(categoryQuery)
    categoriesFilenames = [row[0] for row in categoriesResult]        
    return [categoriesFilenames, categoriesAcross]

def authorResult(db, authors, authorAcross):
    authorsQuery = None
    if len(authors) > 1:
        authorsQuery = text('select distinct metaID from authors_dimension where authorId IN {} ;'.format(authors))
    else:
        authorsQuery = text('select distinct metaID from authors_dimension where authorId = {} ;'.format(authors[0]))

    authorsResult = db.engine.execute(authorsQuery)
    authorsFilenames = [row[0] for row in authorsResult]        
    return [authorsFilenames, authorAcross]

def topicResult(db, topics, topicsAcross):
    topicsQuery = None
    if len(topics) > 1:
        topicsQuery = text('select distinct metaID from topics_dimension where topicId IN {} ;'.format(topics))
    else:
        topicsQuery = text('select distinct metaID from topics_dimension where topicId = {} ;'.format(topics[0]))

    topicsResult = db.engine.execute(topicsQuery)
    topicsFilenames = [row[0] for row in topicsResult]
    return [topicsFilenames, topicsAcross]

def locationResult(db, locations, locationsAcross):
    locationsQuery = None
    if len(locations) > 1:
        locationsQuery = text('select distinct metaID from location_dimension where locationId IN {} ;'.format(locations))
    else:
        locationsQuery = text('select distinct metaID from location_dimension where locationId = {} ;'.format(locations[0]))

    locationsResult = db.engine.execute(locationsQuery)
    locationsFilenames = [row[0] for row in locationsResult]
    return [locationsFilenames, locationsAcross]

def dateResult(db, fromDate, toDate, dateAcross):
    fromDate = fromDate.split('-')
    formattedFromDate = datetime.date(int(fromDate[0]), int(fromDate[1]), int(fromDate[2]))
    toDate = toDate.split('-')
    formattedToDate = datetime.date(int(toDate[0]), int(toDate[1]), int(toDate[2]))

    try:
        dateQuery = text('select distinct metaID from publication where timestamp between "{}" and "{}";'.format(formattedFromDate, formattedToDate))
        dateResult = db.engine.execute(dateQuery)
        dateFilenames = [row[0] for row in dateResult]
        return [dateFilenames, dateAcross]
    except:
        return []