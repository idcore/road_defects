import pymongo
from config import settings

# Establish a connection to the MongoDB server (you may need to specify the connection URL)
client = pymongo.MongoClient(settings.DB_URL)

# Choose a database and collection (replace 'mydb' and 'mycollection' with your database and collection names)
db = client.road_defects
collection = db.coco_data

# Create a dictionary representing your document
document = {
    "video_file": "2.avi",
    "status": "N"
}

# Insert the document into the collection
insert_result = collection.insert_one(document)

# Check if the insertion was successful
if insert_result.acknowledged:
    print("Document inserted successfully.")
    print("Inserted document ID:", insert_result.inserted_id)
else:
    print("Failed to insert document.")

# Close the MongoDB connection when done (optional)
client.close()
