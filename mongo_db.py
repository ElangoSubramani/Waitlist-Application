
import pymongo

client = pymongo.MongoClient("mongodb+srv://Admin:21bda024%40@cluster0.q64wwy9.mongodb.net/")

# Specify the database and collection you want to insert the documents into
db = client.waiting_list
collection = db.customers

# Define the list of documents you want to insert
data = [
    {
        "username": "admin",
        "password": "hashed_password",
        "role": "admin"
    },
    {
        "username": "user1",
        "password": "hashed_password",
        "role": "user"
    },
    {
        "username": "user2",
        "password": "hashed_password",
        "role": "user"
    },
    # Add more user accounts here
]

# Insert the documents into the collection
result = collection.insert_many(data)

# Print the IDs of the inserted documents
print("Inserted document IDs:", result.inserted_ids)
