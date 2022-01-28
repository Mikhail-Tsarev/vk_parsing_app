from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)
db = SQLAlchemy(app)


from app import views
