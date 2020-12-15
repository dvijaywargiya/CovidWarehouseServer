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

class Category(db.Model):
    categoryId = db.Column(db.String(120), primary_key=True)
    categoryName = db.Column(db.String(120), index=True)

class CategoryDimension(db.Model):
    id = db.Column(db.String(120), primary_key=True)
    metaID = db.Column(db.String(120), index=True)
    categoryId = db.Column(db.String(120), db.ForeignKey('category.categoryId'))

class Type(db.Model):
    typeId = db.Column(db.String(120), primary_key=True)
    typeName = db.Column(db.String(120), index=True)

class TypeDimension(db.Model):
    id = db.Column(db.String(120), primary_key=True)
    metaID = db.Column(db.String(120), index=True)
    typeId = db.Column(db.String(120), db.ForeignKey('type.typeId'))

class Topics(db.Model):
    topicId = db.Column(db.String(120), primary_key=True)
    topicName = db.Column(db.String(120), index=True)

class Author(db.Model):
    authorId = db.Column(db.String(120), primary_key=True)
    authorName = db.Column(db.String(120), index=True)

class TopicsDimension(db.Model):
    id = db.Column(db.String(120), primary_key=True)
    metaID = db.Column(db.String(120), index=True)
    topicId = db.Column(db.String(120), db.ForeignKey('topics.topicId'))

class AuthorsDimension(db.Model):
    id = db.Column(db.String(120), primary_key=True)
    metaID = db.Column(db.String(120), index=True)
    authorId = db.Column(db.String(120), db.ForeignKey('author.authorId'))

class Publication(db.Model):
    metaID = db.Column(db.String(120), primary_key=True)
    timestamp = db.Column(db.Date, index=True)

class FileDimension(db.Model):
    metaID = db.Column(db.String(120), primary_key=True)
    fileName = db.Column(db.String(120), index=True)
    title = db.Column(db.Text)
    link = db.Column(db.String(120), index=True)
    abstract = db.Column(db.Text)
    abstractLink = db.Column(db.String(120), index=True)

class Uploads(db.Model):
    fileId = db.Column(db.String(120), primary_key=True)
    timeStamp = db.Column(db.DateTime, index=True)
    ip = db.Column(db.String(120), index=True)
    title = db.Column(db.String(120), index=True)
    link = db.Column(db.String(120), index=True)

class Location(db.Model):
    locationId = db.Column(db.String(120), primary_key=True)
    locationName = db.Column(db.String(120), index=True)

class LocationDimension(db.Model):
    id = db.Column(db.String(120), primary_key=True)
    metaID = db.Column(db.String(120), index=True)
    locationId = db.Column(db.String(120), db.ForeignKey('location.locationId'))
