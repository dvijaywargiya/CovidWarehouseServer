from sqlalchemy import text

def authorResult(db, authors):
    authorsQuery = None
    if len(authors) > 1:
        authorsQuery = text('select distinct metaID from authors_dimension where authorId IN {} ;'.format(authors))
    else:
        authorsQuery = text('select distinct metaID from authors_dimension where authorId = {} ;'.format(authors[0]))

    authorsResult = db.engine.execute(authorsQuery)
    authorsFilenames = [row[0] for row in authorsResult]        
    return [authorsFilenames, authorAcross]
