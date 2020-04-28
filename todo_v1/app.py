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

# Initialize flask migrate
from flask_migrate import Migrate
migrate = Migrate(app, db)


#  model
class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), unique=False, nullable=True)
    completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<TODO.  id: {self.id}, description: {self.description}, completed: {self.completed}>'

#   create
# this should not be called if flask migrate is used
# db.create_all() # create table if not exists




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


@app.route('/todos/update-completed', methods=['POST'])
def update_completed():
  error = False
  body = {}
  try:
    id = request.json['id']
    completed = request.json['completed']
    todo = Todo.query.get(id)
    print(todo)
    todo.completed = completed
    db.session.commit()
    body['description'] = todo.description
    body['id'] = todo.id
    body['completed'] = todo.completed
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
    body['id'] = todo.id
    body['completed'] = todo.completed

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


@app.route('/todos/<id>', methods=['DELETE'])
def remove_todo(id):
  error = False
  try:
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify({"deleted" : "OK"})
 

# MIGRATIONS ==> Flask-Migrate

# Do not have to drop and recreate tables manually (loosing all data!)
# Auto-detects changes from the old version & new version of the SQLAlchemy models
# Creates a migration script that resolves differences between the old & new versions

### how to use? 

# 1 install with pip
# 2 instantiate
# 3 db.create_all() should be removed
# 4 in console: flask db init
# Creating the migrations directory structure using 
# 5 run: flask db migrate - detects changes and craetes migration script
# in migrations directory - versions - new migration script will appear
# 6 flask db upgrade - run to upgrade DB
# in migration script there is also method for downgrade
# 7 flask db downgrade


########################
# Mapping relations
########################

#### One-To-many
# 
# class Todo(db.Model):
#   __tablename__ = 'todos'
#   id = db.Column(db.Integer, primary_key=True)
#   description = db.Column(db.String(), nullable=False)
#   completed = db.Column(db.Boolean, default=False)
#   list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

#   def __repr__(self):
#     return f'<Todo {self.id} {self.description}>'

# class TodoList(db.Model):
#   __tablename__ = 'todolists'
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(), nullable=False)
#   todos = db.relationship('Todo', backref='list', lazy=True)

###### Many-TO-Many
# 
# order_items = db.Table('order_items',
#     db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
#     db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
# )

# class Order(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   status = db.Column(db.String(), nullable=False)
#   products = db.relationship('Product', secondary=order_items,
#       backref=db.backref('orders', lazy=True))

# class Product(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(), nullable=False)