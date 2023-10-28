from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://Admin:21bda024%40@cluster0.q64wwy9.mongodb.net/")  
db_name = "waiting_list_db"
collection_name = "customers"
db = client[db_name]
customer_list_collection = db[collection_name]

current_position = 99
def current_position():
    return current_position
def increment_current_position():
    return current_position + 1
# Generate a unique referral link for a customer

def generate_referral_link(email):
    # You can use a hash function or other unique token generation method here
    # For simplicity, you can use a basic example:
    referral_code = email.replace("@", "").replace(".", "")
    referral_link = f"http://127.0.0.1:5000/refer_friend/signup/{referral_code}"
    return referral_link
# Create a new customer on the waiting list
@app.route('/signup', methods=['POST'])

def signup():
    global current_position

    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Check if the email is already in the waiting list
    if customer_list_collection.find_one({"email": email}):
        return jsonify({"error": "You are already on the waiting list"}), 400

    # Add the customer to the waiting list
    position = current_position
    current_position += 1

    # Generate a unique referral link
    referral_link = generate_referral_link(email)

    # Initialize referral count

    customer_list_collection.insert_one({"email": email, "position": position, "referral_link": referral_link})

    return jsonify({
        "message": "You have been added to the waiting list",
        "position": position,
        "referral_link": referral_link
    }), 201

# Get the position of a customer in the waiting list
@app.route('/position/<email>', methods=['GET'])
def get_position(email):
    customer = customer_list_collection.find_one({"email": email})
    if customer:
        position = customer["position"]
        return jsonify({"position": position}), 200
    else:
        return jsonify({"error": "You are not on the waiting list"}), 404

# Refer a friend and move up the waiting ist
@app.route('/refer_friend/signup/<referral_mail>', methods=['POST'])
def refer_friend(referral_mail): 
    global current_position 
    referral_mail= str(referral_mail)  
    print(referral_mail)
    data=customer_list_collection.find({"email": "new_customerexamplecommy1"})
    print(data)               #customer_list_collection.find_one({"referral_link": referral_link})
    if customer_list_collection.find({"email": referral_mail}):
        email = request.get_json().get('email')
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({"error": "Email is required"}), 400

        # Check if the email is already in the waiting list
        if customer_list_collection.find_one({"email": email}):
            return jsonify({"error": "You are already on the waiting list"}), 400

        # Add the customer to the waiting list
        position = current_position
        current_position += 1

        # Generate a unique referral link
        referral_link = generate_referral_link(email)

        # Initialize referral count

        customer_list_collection.insert_one({"email": email, "position": position, "referral_link": referral_link})

        return jsonify({
            "message": "You have been added to the waiting list",
            "position": position,
            "referral_link": referral_link
        }), 201
    else:

        return jsonify({"error": "Invalid referral link"}), 404

if __name__ == '__main__':
    app.run(debug=True)
