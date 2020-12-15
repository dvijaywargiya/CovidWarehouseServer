from flask import Flask
# from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from os import path
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #     'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://icdw:password@localhost/ICDW'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = '/var/www/CovidWarehouseServer/CovidWarehouseServer/uploads'
    # UPLOAD_FOLDER = './uploads'
    ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

from .populate_incremental import *
from .populate_bulk import *
from .models import *

populateIncremental(db, Category, CategoryDimension, Type, TypeDimension, Location, LocationDimension, Topics, Author, Publication, AuthorsDimension, TopicsDimension, FileDimension)
# populateBulk(db, Category, CategoryDimension, Type, TypeDimension, Location, LocationDimension, Topics, Author, Publication, AuthorsDimension, TopicsDimension, FileDimension)

from . import routes
