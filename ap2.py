 
from flask import Flask, request, jsonify
from pymongo import MongoClient

class WaitingListApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.client = MongoClient("mongodb+srv://Admin:21bda024%40@cluster0.q64wwy9.mongodb.net/") 
        self.db_name = "waiting_list_db"
        self.collection_name = "customers"
        self.db = self.client[self.db_name]
        self.customer_list_collection = self.db[self.collection_name]
        self.current_position = 99

        self.app.route('/signup', methods=['POST'])(self.signup)
        self.app.route('/position/<email>', methods=['GET'])(self.get_position)
        self.app.route('/refer_friend/signup/<referral_mail>', methods=['POST'])(self.refer_friend)

    def generate_referral_link(self, email):
        referral_code = email.replace("@", "").replace(".", "")
        referral_link = f"http://127.0.0.1:5000/refer_friend/signup/{referral_code}"
        return referral_link

    def signup(self):
        data = request.get_json()
        email = data.get('email')
        name= data.get('name')
        password = data.get('password')
        total_refers=0

        if not email or not name or not password:
            return jsonify({"error": "Name , Email & Password is required"}), 400

        if self.customer_list_collection.find_one({"email": email}):
            return jsonify({"error": "You are already on the waiting list"}), 400

        position = self.current_position
        self.current_position += 1

        referral_link = self.generate_referral_link(email)

        self.customer_list_collection.insert_one({"name":name,"email": email,"password":password, "position": position, "referral_link": referral_link,"total_refers":total_refers})

        return jsonify({
            "message": "You have been added to the waiting list",
           "name":name,
           "email": email,
           "password":password,
             "position": position, 
             "referral_link": referral_link,
             "total_refers":total_refers
        }), 201

    def get_position(self, email):
        customer = self.customer_list_collection.find_one({"email": email})
        if customer:
            position = customer["position"]
            return jsonify({"position": position}), 200
        else:
            return jsonify({"error": "You are not on the waiting list"}), 404

    def refer_friend(self, referral_mail):
        referral_mail = str(referral_mail)
        if self.customer_list_collection.find({"email": referral_mail}):
            data = request.get_json()
            email = data.get('email')
            name= data.get('name')
            password = data.get('password')
            total_refers=0

            if not email or not name or not password:
                return jsonify({"error": "Name , Email & Password is required"}), 400

            if self.customer_list_collection.find_one({"email": email}):
                return jsonify({"error": "You are already on the waiting list"}), 400

            position = self.current_position
            self.current_position += 1

            referral_link = self.generate_referral_link(email)

            self.customer_list_collection.insert_one({"name":name,"email": email,"password":password, "position": position, "referral_link": referral_link,"total_refers":total_refers})

            return jsonify({
                "message": "You have been added to the waiting list",
            "name":name,
            "email": email,
            "password":password,
                "position": position, 
                "referral_link": referral_link,
                "total_refers":total_refers
            }), 201

        else:
            return jsonify({"error": "Invalid referral link"}), 404

    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    app = WaitingListApp()
    app.run()
