from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import *

app = Flask(__name__)
app.config.from_object(config_settings['development'])
db = SQLAlchemy(app)
