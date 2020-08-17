from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from os import path

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

from app.populate import populateTopics, populateAuthor, populateFreqItems, populatePublication, populateFact
from app.models import *

populateFact(db, Fact)
populateTopics(db, Topics)
populateAuthor(db, Author)
populateFreqItems(db, FreqItems)
populatePublication(db, Publication)
    

from app import routes