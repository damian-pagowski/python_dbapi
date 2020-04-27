
### syntax - query object

# Model.query - object that allows generating SELECT statements. Every Model has it
# example: Person.query.all() 
# query methods examples: count(), all(), first(), filter(Person.name="Damian), filter_by(name="Damian") <= here is difference between filter and filter_by
# order_by, limit, get(id) [get by ID]
# methods can be chained
# also can be chainde with delete -> that will delete records that are query result
# joins

# SELECT * from persons WHERE name = 'Damian'; >>>  Person.query.filter_by(name='Damian')

# SELECT * from persons; >>> person.query.all()

# SELECT COUNT(*) FROM persons; >>> Person.query.count()

# SELECT * from persons WHERE id = 1; >>> Person.query.get(1)

# SELECT * from persons LIMIT 1 >>> Person.query.limit(1).all()

### Object Lifecycle in SQL alchemy

# 1 ) Transient: an object exists, it was defined.
# person = Person(name="Deku")
# ...but not attached to a session (yet).

# 2 ) Pending: an object was attached to a session. 
# db.session.add(person)
# "Undo" becomes available via db.session.rollback(). Waits for a flush to happen
# also possible to UPDATE just by modifying object attributes: person.name="Goku"

# Flushed: about ready to be committed to the database, translating actions into SQL command statements for the engine.
# changes not commited yet.
# when flush is happening? called automatically by engine before executing commit?
# almost correct, it occurs also when query is called

# Committed: manually called for a change to persist to the database (permanently); session's transaction is cleared for a new set of changes.