# installation
# damian@laptop:~$ pip3 install psycopg2-binary
# damian@laptop:~$ pip3 install flask-sqlalchemy
# damian@laptop:~$ pip3 install flask

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# connection details
POSTGRES_PW='postgres'
POSTGRES_USER='postgres'
POSTGRES_URL='localhost:5432'
POSTGRES_DB='mydb'
# connection URL
DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=False, nullable=True)

db.create_all()