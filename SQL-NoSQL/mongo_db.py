from pymongo import MongoClient
from pprint import pprint

# create a list of articles
articles =[
    {'name':'Hat', 'price': 10.99},
    {'name':'Shirt', 'price': 22.44},
    {'name':'Pullover', 'price': 32.11},
    {'name':'Rubber', 'price': 06.00},
    {'name':'Pan', 'price': 45.99},
]

# create a Mongo client
client = MongoClient('localhost', 27017)

with client:
    # create a database
    db = client.testdb
    # insert all the articles into the database collection called 'articles'
    db.articles.insert_many(articles)
    
    # get all available collection names
    print(db.collection_names())

    """ get a PyMongo cursor and iterate over it """
    arts = db.articles.find()
    for _ in range(3):
    print(arts.next())

    # reset to cursor 
    arts.rewind()

    for _ in range(3):
    print(arts.next())

    print(list(arts))


    """ read all data in the collection """
    for a in arts:
        print(f"name: {a['name']}, price: {a['price']}"")

    """ get infos from the server """
    # get the MongoDB server's status
    print(db.command('serverStatus'))

    # get the server's statistics
    print(db.command('dbstats'))


    # remove the collection 'articles'
    db.articles.drop()