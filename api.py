from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://Admin:21bda024%40@cluster0.q64wwy9.mongodb.net/")  # Replace with your MongoDB connection string
db = client["mydatabase"]  # Replace with your database name
collection = db["mycollection"]  # Replace with your collection name

# Create a new document
@app.route("/create", methods=["POST"])
def create_document():
    data = request.json
    if data:
        document_id = collection.insert_one(data).inserted_id
        return jsonify({"message": "Document created", "document_id": str(document_id)}), 201
    else:
        return jsonify({"error": "Invalid request data"}), 400

# Read a document by ID
@app.route("/read/<document_id>", methods=["GET"])
def read_document(document_id):
    document = collection.find_one({"_id": document_id})
    if document:
        return jsonify(document), 200
    else:
        return jsonify({"error": "Document not found"}), 404

# Update a document by ID
@app.route("/update/<document_id>", methods=["PUT"])
def update_document(document_id):
    data = request.json
    if data:
        result = collection.update_one({"_id": document_id}, {"$set": data})
        if result.modified_count > 0:
            return jsonify({"message": "Document updated"}), 200
        else:
            return jsonify({"error": "Document not found or no changes made"}), 404
    else:
        return jsonify({"error": "Invalid request data"}), 400

# Delete a document by ID
@app.route("/delete/<document_id>", methods=["DELETE"])
def delete_document(document_id):
    result = collection.delete_one({"_id": document_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Document deleted"}), 200
    else:
        return jsonify({"error": "Document not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
