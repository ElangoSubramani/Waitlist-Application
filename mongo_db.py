import pymongo 

# Replace the following with your MongoDB Atlas connection string
# You can find your connection string in the MongoDB Atlas dashboard.
# mongo_uri = "your_mongodb_atlas_connection_string"

# Create a MongoDB client
client = pymongo.MongoClient("mongodb+srv://Admin:21bda024@@cluster0.q64wwy9.mongodb.net/")

# Access a specific database
db = client["your_database_name"]

# Access a specific collection within the database
collection = db["your_collection_name"]

# Now you can perform various database operations using the "collection" object
# For example, you can insert a document into the collection:
data = {"key": "value"}
collection.insert_one(data)

# Close the MongoDB connection when you're done
client.close()
