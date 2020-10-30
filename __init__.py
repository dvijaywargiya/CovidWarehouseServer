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

from .populate import *
from .models import *

# populateType(db, Type)
# populateTypeDimension(db, TypeDimension)
# populateLocation(db, Location)
# populateLocationsDimension(db, LocationDimension)
# populateTopics(db, Topics)
# populateAuthor(db, Author)
# populatePublication(db, Publication)
# populateAuthorDimension(db, AuthorsDimension)
# populateTopicsDimension(db, TopicsDimension)
# populateFileDimension(db, FileDimension)

from . import routes
