from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

#laddar data från .env
load_dotenv()

app = Flask(__name__)
#sätter database_uri till tests.db eller library.db beroende på om TESTING är True eller False i .env-filen
database_uri='sqlite:///tests.db' if os.environ.get('TESTING')=='True' else 'sqlite:///library.db'
app.config['SQLALCHEMY_DATABASE_URI']= database_uri
db = SQLAlchemy(app)

from app import routes