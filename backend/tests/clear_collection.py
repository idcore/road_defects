import pymongo
from config import  settings

# Establish a connection to the MongoDB server (you may need to specify the connection URL)
client = pymongo.MongoClient(settings.DB_URL)

# Choose a database and collection (replace 'mydb' and 'mycollection' with your database and collection names)
db = client.road_defects
collection = db.tasks

collection.delete_many({})

client.close()
