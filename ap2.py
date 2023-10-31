

"""

FileName: api_serer.py
Author: ELANGO S
Created Date: 27-10-2023
Description: This file is used to create a REST API server using Flask.
packages: flask, pymongo
class: WaitingListApp
functions: signup, get_position, refer_friend, run


"""


#Importing the required packages

from flask import Flask, request, jsonify
from pymongo import MongoClient
#Creating a class WaitingListApp
class WaitingListApp:
    #Initializing the class using __init__ method(constructer)
    def __init__(self):
        #Creating a Flask app
        self.app = Flask(__name__)
        #Creating a MongoDB connection using MongoClient the connection string is passed as an argument to the MongoClient constructor
        #The connection string is obtained from the MongoDB Atlas dashboard
        #The connection string contains the username and password of the database user
        self.client = MongoClient("mongodb+srv://Admin:21bda024%40@cluster0.q64wwy9.mongodb.net/") 
        #The name of the database and the collection are stored in variables

        self.db_name = "waiting_list_db"
        self.collection_name = "customers"
        self.db = self.client[self.db_name]
        #The list of collections in the database are obtained using the list_collection_names() method
        #If the collection doesn't exist, it is created using the insert_many() method
        if not  self.collection_name in self.db.list_collection_names():
            self.initialize_database()
            
        #The collection is stored in a variable
        self.customer_list_collection = self.db[self.collection_name]
        #The current position is stored in a variable and is initialized to 99
        self.current_position = 99
        #The routes are defined using the route() decorator
        #The signup() method is called when the /signup route is accessed using the POST method
        self.app.route('/signup', methods=['POST'])(self.signup)
        #The get_position() method is called when the /position/<email> route is accessed using the GET method
        self.app.route('/position/<email>', methods=['GET'])(self.get_position)
        #The refer_friend() method is called when the /refer_friend/signup/<referral_mail> route is accessed using the POST method
        self.app.route('/refer_friend/signup/<referral_mail>', methods=['POST'])(self.refer_friend)
    def initialize_database(self):
        db = self.client.waiting_list_db
        collection = db.customers

        # Define the list of documents you want to insert
        data = [
            {
                "username": "admin",
                "password": "hashed_password",
                "role": "admin"
            },
        
        ]

        # Insert the documents into the collection
        result = collection.insert_many(data)

        # Print the IDs of the inserted documents
        print("Created database:", result.inserted_ids)


    def generate_referral_link(self, email):
        referral_code = email.replace("@", "$").replace(".", "&")
        referral_link = f"http://127.0.0.1:5000/refer_friend/signup/{referral_code}"
        return referral_link

    def update_customer(self, email, position, total_referrals):
        # Find the customer in the collection
        customer = self.customer_list_collection.find_one({"email": email})
        
        if customer:
            # Update the position and total_referrals fields
            self.customer_list_collection.update_one(
                {"email": email},
                {
                    "$set": {
                        "position": position,
                        "total_referrals": total_referrals
                    }
                }
            )



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
             "total_referrals":total_refers
        }), 201

    def get_position(self, email):
        customer = self.customer_list_collection.find_one({"email": email})
        if customer:
            position = customer["position"]
            return jsonify({"position": position}), 200
        else:
            return jsonify({"error": "You are not on the waiting list"}), 404

    def refer_friend(self, referral_mail):
        referral_mail = referral_mail.replace("$", "@").replace("&", ".")
        customer = self.customer_list_collection.find_one({"email": referral_mail})
        if customer:
            data = request.get_json()
            email = data.get('email')
            name= data.get('name')
            password = data.get('password')
            total_refers=0
            print(customer["position"])
            updated_postion=customer["position"]-1
            updated_total_refers=customer["total_refers"]+1

         # update_operation = {"$set": {"position": customer["position"]-1, "total_refers": customer[total_refers]+1}}
            # updated_status=self.customer_list_collection.find_one_and_update({"email": referral_mail},update_operation,return_document=True)
            # if updated_status==True:
            #     print("updated")
            # else:
                # print("not updated")  

            if not email or not name or not password:
                return jsonify({"error": "Name , Email & Password is required"}), 400

            if self.customer_list_collection.find_one({"email": email}):
                return jsonify({"error": "You are already on the waiting list"}), 400
#update the position and total_referrals fields of the existing customer which is referral_mail
            self.customer_list_collection.update_one(
                {"email": referral_mail},
                {
                    "$set": {
                        "position": updated_postion,
                        "total_referrals": updated_total_refers
                    }
                }
            )
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
