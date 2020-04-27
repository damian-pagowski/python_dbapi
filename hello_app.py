from flask import Flask

app = Flask(__name__)

# @app is called decorator
# prenaunciation [raut]
# running app: FLASK_APP=hello_app.py flask run
# FLAG=value this is called flag, have to be declared with = without spaces
# export FLASK_ENV=development
# 
##########################

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

#model
class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=False, nullable=True)

    def __repr__(self):
        return f'<The User. Details >> id: {self.id}, name: {self.name}>'


#create
db.create_all()
##########################

@app.route('/')
def index():
    person = Person.query.first()
    return 'Hello ' + person.name

if __name__ == '__main__':
    app.run()