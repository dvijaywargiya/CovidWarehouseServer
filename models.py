from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

class User(db.Model):
    userId = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    token = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Fact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metaId = db.Column(db.Integer, index=True)
    arxivId = db.Column(db.String(64), index=True)
    title = db.Column(db.String(128), index=True)
    pdfLink = db.Column(db.String(128), index=True)
    abstract = db.Column(db.String(512), index=True)
    abstractLink = db.Column(db.String(128), index=True)
    authors = db.Column(db.String(512), index=True)
    publishedDate = db.Column(db.String(32), index=True)
    link = db.Column(db.String(512), index=True)
    tag = db.Column(db.String(512), index=True)

class Topics(db.Model):
    topicId = db.Column(db.Integer, primary_key=True)
    topicName = db.Column(db.String(120), index=True)

class Author(db.Model):
    authorId = db.Column(db.Integer, primary_key=True)
    authorName = db.Column(db.String(120), index=True)

class TopicsDimension(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(120), index=True)
    topicId = db.Column(db.Integer, db.ForeignKey('topics.topicId'))

class AuthorsDimension(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(120), index=True)
    authorId = db.Column(db.Integer, db.ForeignKey('author.authorId'))

class FreqItems(db.Model):
    itemSetId = db.Column(db.Integer, primary_key=True)
    itemSet = db.Column(db.String(1024), index=True)

class Publication(db.Model):
    fileId = db.Column(db.String, primary_key=True)
    date = db.Column(db.String(1024), index=True)