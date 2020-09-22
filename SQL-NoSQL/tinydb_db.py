from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

# create a database
db = TinyDB(storage=MemoryStorage)

# insert elements into the database
db.insert({'id': 1, 'first_name': 'Tim', 'last_name': 'Hu'})
db.insert({'id': 2, 'first_name': 'Luke', 'last_name': 'Hu'})

# read all entries
print(db. all())
for item in db:
    print(item)

# read the entry for a specified first_name or an id greater than zero
User = Query()
print(db.search(User.first_name == 'Tim'))
print(db.search(User.id > 0))

# update an entry
db.update({'first_name': 'Scott'}, User.id == 1)
print(db.all())

# remove entries
db.remove(User.id > 1)
print(db.all())

# reset the database
db.purge()
print(db.all())

