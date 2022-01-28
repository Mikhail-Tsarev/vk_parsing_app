import os

from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

TOKEN = os.getenv("TOKEN")


class Configuration(object):
    DEBUG = True
    SECRET_KEY = "'dfh323!@#?"
    DATABASE = "sqlite:///data.db"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")
