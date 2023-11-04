

"""

FileName: api_serer.py
Author: ELANGO S
Created Date: 27-10-2023
Description: This file is used to create a REST API server using Flask.
packages: flask, pymongo
class: WaitingListApp
functions: signup, get_position, refer_friend, run
Database: MongoDB Atlas

"""

# Importing the required packages

from flask import Flask, request, jsonify
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from environs import Env
# Creating a class WaitingListApp


class WaitingListApp:
    # Initializing the class using __init__ method(constructer)
    def __init__(self):
        # Creating a Flask app
        self.app = Flask(__name__)
        # Creating a MongoDB connection using MongoClient the connection string is passed as an argument to the MongoClient constructor
        # The connection string is obtained from the MongoDB Atlas dashboard
        # The connection string contains the username and password of the database user
        # This is super duper important to replce the username and password with the actual username and password of the database user
        self.env = Env()
        self.env.read_env("environments.env")
        self.client = MongoClient(self.env("MONGODB_ACCESS_KEY")
            )
        # The name of the database and the collection are stored in variables

        self.db_name = "waiting_list_db"
        self.collection_name = "customers"
        self.db = self.client[self.db_name]
        # The list of collections in the database are obtained using the list_collection_names() method
        # If the collection doesn't exist, it is created using the insert_many() method
        if not self.collection_name in self.db.list_collection_names():
            self.initialize_database()

        # The collection is stored in a variable
        self.customer_list_collection = self.db[self.collection_name]
        # The current position is stored in a variable and is initialized to 99
        self.current_position = 99
        # The routes are defined using the route() decorator
        # The signup() method is called when the /signup route is accessed using the POST method
        self.app.route('/signup', methods=['POST'])(self.signup)
        # The login() method is called when the /login/<email> route is accessed using the POST method
        self.app.route('/login/<email>/<password>',
                       methods=['GET'])(self.login)
        # The get_user_login_data() method is called when the /get_user_login_data/<email> route is accessed using the GET method
        self.app.route('/get_user_login_data/<email>',
                       methods=['GET'])(self.get_user_login_data)
        # The refer_friend() method is called when the /refer_friend/signup/<referral_mail> route is accessed using the POST method
        self.app.route('/refer_friend/signup/<referral_mail>',
                       methods=['POST'])(self.refer_friend)
        self.app.route('/admin_login/<email>/<password>',
                       methods=['GET'])(self.admin_login)
        self.app.route('/update_user/<email>',
                       methods=['PUT'])(self.update_user)
        self.app.route('/delete_user/<email>',
                       methods=['DELETE'])(self.delete_user)

    # The initialize_database() method is used to create the database and insert the documents into the collection
    def initialize_database(self):
        # Create the database
        db = self.client.waiting_list_db
        # Specify the database and collection you want to insert the documents into
        collection = db.customers

        # Define the list of documents you want to insert
        data = [
            {
                "email": "admin@gmail.com",
                "name": "ELANGO S",
                "password": "admin",
                "position": 99,
                "referral_link": "http://127.0.0.1:5000/refer_friend/signup/admin@gmail.com",
                "total_refers": 0


            }

        ]

        # Insert the documents into the collection
        result = collection.insert_many(data)

        # Print the IDs of the inserted documents
        print("Created database:", result.inserted_ids)

    # The generate_referral_link() method is used to generate the referral link
    def generate_referral_link(self, email):
        # The email address is used to generate the referral link
        referral_code = email.replace("@", "$").replace(".", "&")
        # The referral link is returned
        referral_link = f"http://127.0.0.1:5000/refer_friend/signup/{referral_code}"
        return referral_link
    # The update_customer() method is used to update the position and total_refers fields of the existing customer

    def update_customer(self, email, position, total_refers):
        # Find the customer in the collection
        customer = self.customer_list_collection.find_one({"email": email})
        # If the customer exists

        if customer:
            # Update the position and total_refers fields
            self.customer_list_collection.update_one(
                # The email address is used to find the customer
                {"email": email},
                {
                    # The position and total_refers fields are updated
                    "$set": {
                        "position": position,
                        "total_refers": total_refers
                        # The updated customer details are returned
                    }
                }
            )

    # The signup() method is used to add a new customer to the waiting list

    def signup(self):
        # The request data is obtained using the get_json() method
        data = request.get_json()
        # The email, name and password are obtained from the request data
        email = data.get('email')
        # The email address is used to generate the referral link
        name = data.get('name')
        # The email address is used to generate the referral link
        password = data.get('password')
        # The email address is used to generate the referral link
        total_refers = 0
        # If the email, name or password is not provided, an error message is returned
        # The HTTP status code 400 is used to indicate a bad request

        if not email or not name or not password:
            return jsonify({"error": "Name , Email & Password is required"}), 400
        # If the customer already exists, an error message is returned
        # The HTTP status code 400 is used to indicate a bad request
        if self.customer_list_collection.find_one({"email": email}):
            return jsonify({"error": "You are already on the waiting list"}), 400
        # The position is incremented by 1
        # The current position is stored in a variable and is initialized to 99
        position = self.current_position
        # The current position is stored in a variable and is initialized to 99
        self.current_position += 1
        # The referral link is generated using the generate_referral_link() method
        # The referral link is stored in a variable called referral_link

        referral_link = self.generate_referral_link(email)

        # The customer is added to the waiting list

        self.customer_list_collection.insert_one({"name": name, "email": email, "password": password,
                                                 "position": position, "referral_link": referral_link, "total_refers": total_refers})
        # The customer details are returned
        return jsonify({
            "message": "You have been added to the waiting list",
            "name": name,
            "email": email,
            "password": password,
            "position": position,
            "referral_link": referral_link,
            "total_refers": total_refers
        }), 201  # The HTTP status code 201 is used to indicate a successful request

    def login(self, email, password):

        # The email address is used to find the customer in the collection
        customer = self.customer_list_collection.find_one({"email": email})
        if customer == None:
            return jsonify({"error": "Incorrect Email Id"}), 404
        # password is checked
        if password == customer["password"]:
            # data= self.get_user_login_data(email)

            #    return data
            return jsonify({


                "text": "Welcome" + customer["name"],

            }), 200
        else:
            # If the customer doesn't exist, an error message is returned
            return jsonify({"Incorrect password"}), 404

    def get_user_login_data(self, email):
        # The email address is used to find the customer in the collection
        customer = self.customer_list_collection.find_one({"email": email})
        # If the customer exists
        if customer:
            # The position is obtained from the customer details
            position = customer["position"]
            # The customer details are returned
            return jsonify({

                "name": customer["name"],
                "email": customer["email"],
                "total_refers": customer["total_refers"],
                "referral_link": customer["referral_link"],
                "position": position}), 200
        else:
            # If the customer doesn't exist, an error message is returned
            return jsonify({"error": "You are not on the waiting list"}), 404
    # The refer_friend() method is used to add a new customer to the waiting list using a referral link

    def get_user_data(self, email):
        # The email address is used to find the customer in the collection
        customer = self.customer_list_collection.find_one({"email": email})
        # If the customer exists
        if customer:
            # The position is obtained from the customer details
            position = customer["position"]
            # The customer details are returned
            return {

                "name": customer["name"],
                "email": customer["email"],
                "password": customer["password"],
                "total_refers": customer["total_refers"],
                "referral_link": customer["referral_link"],
                "position": position}
        else:
            # If the customer doesn't exist, an error message is returned
            return ({"error": "You are not on the waiting list"})

    def admin_login(self, email, password):

        # The email address is used to find the customer in the collection
        customer = self.customer_list_collection.find_one({"email": email})
        # The email address is used to find the customer in the collection
        all_customers = (self.customer_list_collection.find({}))
        if not customer:
            # If the customer doesn't exist, an error message is returned
            return jsonify({"error": "Incorrect Email Id"}), 404
        # password is checked
        if password == customer["password"]:
            # initialize a  empty list
            ls = []
            # The email address is used to find the customer in the collection
            for customer in all_customers:
                ls.append(self.get_user_data(customer["email"]))

            return jsonify({"all_user_data": ls
                            }), 201

        else:
            # If the customer doesn't exist, an error message is returned
            return jsonify({"error": "Incorrect password"}), 404

    def refer_friend(self, referral_mail):
        # The referral link is decoded to obtain the email address
        # The email address is used to find the customer in the collection
        referral_mail = referral_mail.replace("$", "@").replace("&", ".")
        customer = self.customer_list_collection.find_one(
            {"email": referral_mail})
        # If the customer exists (True)
        if customer:
            # The request data is obtained using the get_json() method
            data = request.get_json()
            # The email, name and password are obtained from the request data
            # The email address is used to generate the referral link
            email = data.get('email')
            name = data.get('name')
            password = data.get('password')
            # initializing the position and total_refers fields of the new customer
            total_refers = 0
            updated_postion = customer["position"]-1
            updated_total_refers = customer["total_refers"]+1
            if updated_postion == 1:
                self.send_email(referral_mail)

            """

         # update_operation = {"$set": {"position": customer["position"]-1, "total_refers": customer[total_refers]+1}}
            # updated_status=self.customer_list_collection.find_one_and_update({"email": referral_mail},update_operation,return_document=True)
            # if updated_status==True:
            #     print("updated")
            # else:
                # print("not updated")  


            """

            if not email or not name or not password:
                return jsonify({"error": "Name , Email & Password is required"}), 400

            if self.customer_list_collection.find_one({"email": email}):
                return jsonify({"error": "You are already on the waiting list"}), 400
            # update the position and total_refers fields of the existing customer which is referral_mail
            self.customer_list_collection.update_one(
                # The email address is used to find the customer
                {"email": referral_mail},
                {
                    # `$set` operator replaces the value of a field with the specified value.
                    "$set": {
                        "position": updated_postion,
                        "total_refers": updated_total_refers
                    }
                }
            )
            # The position is incremented by 1
            position = self.current_position
            self.current_position += 1
            # The referral link is generated using the generate_referral_link() method

            referral_link = self.generate_referral_link(email)
            # The customer is added to the waiting list

            self.customer_list_collection.insert_one(
                {"name": name, "email": email, "password": password, "position": position, "referral_link": referral_link, "total_refers": total_refers})
            # The customer details are returned
            return jsonify({
                "message": "You have been added to the waiting list",
                "name": name,
                "email": email,
                "password": password,
                "position": position,
                "referral_link": referral_link,
                "total_refers": total_refers
            }), 201

        else:
            # If the customer doesn't exist, an error message is returned
            return jsonify({"error": "Invalid referral link"}), 404

    def send_email(self, mail):

        # Your Gmail account credentials
        gmail_user = "elanbit@gmail.com"
        gmail_password = "abcd1234@"
        subject = "You won a prize"
        recipient = mail
        message = "Congratulations! you reached a top position in the leaderboard, You won brand new iPhone 15 Pro Max."

        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        try:
            # Connect to the SMTP server (Gmail's SMTP server in this example)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(gmail_user, gmail_password)

            # Send the email
            text = msg.as_string()
            server.sendmail(gmail_user, recipient, text)
            server.quit()

            print("Email sent successfully")
        except Exception as e:
            print(f"Email sending failed: {str(e)}")

    # The run() method is used to run the Flask app
    def update_user(self, email):
        # Get the updated data from the request
        data = request.get_json()

        # Find the user by their email
        user = self.customer_list_collection.find_one({"email": email})

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Update user data
        updated_data = {
            # Update name if provided, else keep the same
            "name": data.get("name"),
            # Update password if provided, else keep the same
            "password": data.get("password"),
            "position": data.get("position"),
            "referral_link": data.get("referral_link"),
            "total_refers": data.get("total_refers"),

        }

        # Perform the update in the database
        self.customer_list_collection.update_one(
            {"email": email}, {"$set": updated_data})

        return jsonify({"message": "User updated successfully", "user": updated_data}), 200

    def delete_user(self, email):
        # Find the user by their email
        user = self.customer_list_collection.find_one({"email": email})

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Delete the user from the database
        self.customer_list_collection.delete_one({"email": email})

        return jsonify({"message": "User deleted successfully"}), 200

    def run(self):
        # The debug mode is enabled
        self.app.run(debug=True)


# The main() function is used to create an instance of the WaitingListApp class and run the Flask app
if __name__ == '__main__':
    # An instance of the WaitingListApp class is created
    app = WaitingListApp()
    # With the instance, the run() method is called to run the Flask app
    app.run()
