from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app import config

app = Flask(__name__)
app.config.from_object(config.ProductionConfig)
db = SQLAlchemy(app)
