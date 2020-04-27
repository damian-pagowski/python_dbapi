from flask import Flask, render_template, request, redirect, url_for, abort, jsonify

app = Flask(__name__)


# flask looking for templates in /templates directory
# templating language used here is caled jinja

### PSQL pi--si-kju-el
# PSQL COMMAND TO CREATE DAPABASE:
# postgres=# CREATE DATABASE "todo";
# important to use ""
# \l >> list databases
# \c dbname  >> connect to database
# \d >> list tables

from flask_sqlalchemy import SQLAlchemy

# connection details
POSTGRES_PW='postgres'
POSTGRES_USER='postgres'
POSTGRES_URL='localhost:5432'
POSTGRES_DB='todo'
# build connection URL
DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
#  connect to db
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)

#  model
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), unique=False, nullable=True)

#   create
db.create_all() # create table if not exists




################
# GET DATA FROM REQUESTS
#
# 1) query params - GET request
#   ?param1=value
#  request.args.get('param1')
# 2) form 
#   request.form.get('username')
# 3) JSON
#   data_string = request.data
#   data_dictionary = json.loads(data_string)


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())

@app.route('/create-todo', methods=['POST'])
def create_todo():
    todo = Todo(description=request.form.get('description'))
    db.session.add(todo)
    db.session.commit()
    print("create-todo CALLED: " + request.form.get('description'))
    return redirect(url_for('index'))


# ...
import sys

@app.route('/todos/create', methods=['POST'])
def create_todo_json():
  error = False
  body = {}
  try:
    description = request.json['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)
