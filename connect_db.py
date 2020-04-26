import psycopg2

conn = psycopg2.connect("dbname=mydb user=postgres host=localhost password=postgres port=5432")


cursor = conn.cursor()

# Open a cursor to perform database operations
cur = conn.cursor()

# drop any existing todos table
cur.execute("DROP TABLE IF EXISTS todos;")

# (re)create the todos table
# (note: triple quotes allow multiline text in python)
cur.execute("""
  CREATE TABLE todos (
    id serial PRIMARY KEY,
    description VARCHAR NOT NULL
  );
""")

# commit, so it does the executions on the db and persists in the db

# example 2


cursor = cur
cursor.execute('DROP TABLE IF EXISTS table2;')
# create table
cursor.execute('''
  CREATE TABLE table2 (
    id INTEGER PRIMARY KEY,
    completed BOOLEAN NOT NULL DEFAULT False
  );
''')
#insert
cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (1, True))
# insert - another row
SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'

data = {
  'id': 2,
  'completed': False
}
cursor.execute(SQL, data)
# select
cursor.execute('SELECT * FROM table2')

result = cursor.fetchall()
print(result)
# commit and close db
conn.commit()

cur.close()
conn.close()