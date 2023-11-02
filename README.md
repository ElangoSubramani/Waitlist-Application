<img src="./images/logo.sample.png" alt="Logo of the project" align="right">

# WaitList Application:-

This is the Waitlist Application backend and api developed for Cartrabit.

## Installation

### MongoDB Atlas

To get started, you need to set up a MongoDB Atlas cluster and obtain the database access string. Follow these steps:

1. Create a MongoDB Atlas account and sign in.

2. Create a new cluster and configure it according to your needs.

3. Once your cluster is up and running, click the "Connect" button.

4. Copy the provided database access string.

### Setting up the Development Environment

Before you can start developing this project, you need to set up your development environment. Make sure you have the following prerequisites installed:

- Python 3.9 or you can deploy it o your own server
- MongoDB Compass
- [Link to MongoDB Compass](https://www.mongodb.com/try/download/compass)
- Other global dependencies or tools as needed.

Follow these steps to start developing:

1. Clone the project repository:

```shell
git clone https://github.com/your/your-project.git
cd your-project/
```


2. Install the project dependencies using the following command:

```shell

pip install -r requirements.txt 

```

## MongoDB Atlas Setup

1. Open MongoDB Compass and connect to your MongoDB Atlas cluster using the access string you copied earlier.

2. Update the Python program with your database access string.

## Deployment and API Testing

After completing the development setup, you can deploy the project and test the APIs using Postman. Here are the detailed steps:

### Deployment

1. Ensure that your Python program is correctly updated with the database access string.

```shell
   python app.py
   ```

Your API should now be running locally. By default, Flask applications run on localhost (127.0.0.1) and port 5000.
Testing APIs with Postman
Open Postman on your local machine. If you don't have Postman installed, you can download it from Postman's official website.

You'll use Postman to make HTTP requests to your locally running API.

To test a specific endpoint, follow these steps:

a. Open Postman and create a new request.

b. In the request type dropdown, select the appropriate HTTP method (e.g., GET, POST, PUT, DELETE) that corresponds to the API endpoint you want to test.

c. In the request URL field, enter the URL of your local API. By default, it will be something like:

bash
Copy code
http://localhost:5000/api
Replace /api/endpoint with the actual route of the API endpoint you want to test.

d. If your API requires authentication, make sure to provide the necessary credentials in the request headers or authorization settings.

e. If your API requires input data (e.g., for a POST request), add the data to the request body.

f. Click the "Send" button to make the request. Postman will display the response from your API.

Example Test
Suppose you have an API endpoint to retrieve a list of users, and it's accessible at http://localhost:5000/api/users. Here's how you can test it using Postman:

Open Postman.

Create a new request and select the GET method.

Enter http://localhost:5000/api/users in the request URL.

Click "Send."

You should receive a response from your API containing the list of users.

Testing Other Endpoints
Repeat the same process for other API endpoints as need