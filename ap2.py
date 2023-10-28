from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://Admin:21bda024%40@cluster0.q64wwy9.mongodb.net/")  
db = client["Waiting_listdb"]  
waiting_list_collection = db["waiting_list"]
referrals_collection = db["referrals"]

# Default waiting list position
current_position = 99
def generate_referral_link(email):
    # You can use a hash function or other unique token generation method here
    # For simplicity, you can use a basic example:
    referral_code = email.replace("@", "").replace(".", "")
    referral_link = f"https://example.com/signup?referral={referral_code}"
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
    if waiting_list_collection.find_one({"email": email}):
        return jsonify({"error": "You are already on the waiting list"}), 400

    # Add the customer to the waiting list
    position = current_position
    current_position += 1

    # Generate a unique referral link
    referral_link = generate_referral_link(email)

    # Initialize referral count
    referrals_collection.insert_one({"referral_link": referral_link, "count": 0})

    waiting_list_collection.insert_one({"email": email, "position": position, "referral_link": referral_link})

    return jsonify({
        "message": "You have been added to the waiting list",
        "position": position,
        "referral_link": referral_link
    }), 201

# Get the position of a customer in the waiting list
@app.route('/position/<email>', methods=['GET'])
def get_position(email):
    customer = waiting_list_collection.find_one({"email": email})
    if customer:
        position = customer["position"]
        return jsonify({"position": position}), 200
    else:
        return jsonify({"error": "You are not on the waiting list"}), 404

# Refer a friend and move up the waiting list
@app.route('/refer/<referral_link>', methods=['POST'])
def refer_friend(referral_link):
    referral = referrals_collection.find_one({"referral_link": referral_link})
    if referral:
        email = request.get_json().get('email')
        if email:
            # Check if the email is already on the waiting list
            if waiting_list_collection.find_one({"email": email}):
                return jsonify({"error": "Your friend is already on the waiting list"}), 400

            # Add the friend to the waiting list
            position = referral["count"] + 99
            waiting_list_collection.insert_one({"email": email, "position": position, "referral_link": referral_link})

            # Increment the referrer's referral count
            referrals_collection.update_one({"referral_link": referral_link}, {"$inc": {"count": 1}})

            return jsonify({
                "message": "Your friend has been added to the waiting list",
                "position": position
            }), 201

    return jsonify({"error": "Invalid referral link"}), 404

if __name__ == '__main__':
    app.run(debug=True)
