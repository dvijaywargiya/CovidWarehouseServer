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
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

from .populate import populateFileDimension,populateTopics, populateAuthor, populateFreqItems, populatePublication, populateFact, populateAuthorDimension, populateTopicsDimension
from .models import *

# populateFact(db, Fact)
# populateTopics(db, Topics)
# populateAuthor(db, Author)
# populateFreqItems(db, FreqItems)
# populatePublication(db, Publication)
# populateAuthorDimension(db, AuthorsDimension)
# populateTopicsDimension(db, TopicsDimension)
# populateFileDimension(db, FileDimension)

from . import routes
