
import pymongo
import smtplib
from email.mime.text import MIMEText

client = pymongo.MongoClient("mongodb+srv://Admin:21bda024%40@cluster0.q64wwy9.mongodb.net/")
db = client["waiting_list"]

# Define the customers collection
customers = db["customers"]

# Initialize position counter
position = 99

# Initialize email server (replace with your SMTP server details)
smtp_server = "your_smtp_server.com"
smtp_port = 587
smtp_username = "your_username"
smtp_password = "your_password"

# Function to sign up a new customer
def sign_up_customer(email):
    global position
    position += 1

    referral_link = generate_referral_link(email)
    customer = {
        "email": email,
        "position": position,
        "referral_link": referral_link,
        "referrals": [],
    }
    customers.insert_one(customer)

    return customer

# Function to generate a unique referral link
def generate_referral_link(email):
    return f"https://example.com/signup?referral={email}"

# Function to handle a referral
def handle_referral(referrer_email, friend_email):
    referrer = customers.find_one({"email": referrer_email})
    friend = customers.find_one({"email": friend_email})

    if referrer and friend:
        customers.update_one(
            {"email": referrer_email},
            {
                "$push": {
                    "referrals": {"friend_email": friend_email}
                }
            }
        )

# Function to send an email notification
def send_email_notification(customer):
    subject = "Congratulations! You've Reached Position 1"
    message = "You can now purchase the new product with a coupon code."
    
    msg = MIMEText(message)
    msg["From"] = "your_email@example.com"
    msg["To"] = customer["email"]
    msg["Subject"] = subject

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(msg["From"], msg["To"], msg.as_string())
    server.quit()

# Example usage
if __name__ == "__main__":
    # New customer sign-up
    new_customer = sign_up_customer("new_customer@example.com")
    print(f"New Customer: {new_customer}")

    # Handle a referral
    handle_referral("referrer@example.com", "friend@example.com")

    # Check if a customer has reached Position 1 and send email notification
    if new_customer["position"] == 1:
        send_email_notification(new_customer)
