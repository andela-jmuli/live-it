from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import *


app = Flask(__name__)
# config for dev
db = SQLAlchemy(app)
