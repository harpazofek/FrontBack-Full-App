import os
import logging
from pymongo import MongoClient
from flask import Flask, request, jsonify
from logging.handlers import RotatingFileHandler
from logconfig import setup_logging

# Set up logging
setup_logging()

app = Flask(__name__)

# Get MongoDB credentials from environment variables
MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

# Configure the MongoDB connection
client = MongoClient(f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@database-service:27017/")
logging.info(client)

# Access a specific database
db = client["request_db"]
collection = db["requests"]

def testdb():
    try:
        client.command('ismaster')
        logging.debug(client)
    except:
        return "Server not available"
    return "Hello from the MongoDB client!\n"

def save_request():
    try:
        # Extract data from the request
        data = {
            "method": request.method,
            "url": request.url,
            "headers": dict(request.headers),
            "data": request.data.decode('utf-8')
        }

        # Insert data into MongoDB collection
        result = collection.insert_one(data)

        return jsonify({"message": "Request saved", "request_id": str(result.inserted_id)}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

########### Application Routing #############

@app.route('/ping', methods=['GET'])
@app.route('/pong', methods=['POST'])
@app.route('/save_request', methods=['POST', 'GET'])
@app.route('/basic_info', methods=['GET'])
@app.route('/basic_info_add', methods=['POST'])
@app.route('/basic_info_put', methods=['PUT'])
@app.route('/basic_info_del', methods=['DELETE'])

def pingpongfun():
    if request.method == 'GET':
        return '<h1> Ofek say\'s P1NG</h1>'
    if request.method == 'POST':
        return '<h1> Ofek say\'s P0NG</h1>'

@app.route('/ping', methods=['GET'])
def ping():
    if request.method == "GET":
        return f'<H2> Method GET, you have pinged successfuly   <br><br> Have a nice DAY and pong to you <H2> \
                URL: {request.host_url}ping \
                <br><br> Project BY : Daniel, Eli, Ofek, Lior'  


@app.route('/pong', methods=['POST'])
def pong():
    if request.method == "POST":
        return f'<H2> Method POST, you have pinged successfuly  <br><br> Have a nice DAY <H2> \
               URL: {request.host_url}pong \
                <br><br> Project BY : Daniel, Eli, Ofek, Lior'  

# Storage for basic information
basic_info = [
        {"name": "Eli Levi", "city": "Rosh Hain", "ID": 331546518},
        {"name": "Daniel Shahnovich", "city": "Karnei Shomron", "ID": 324578981},
        {"name": "Lior Taub", "city": "Ramat Gan", "ID": 615478536},
        {"name": "Ofek Harpaz", "city": "Tel Aviv", "ID": 308696938},
    ]

@app.route('/basic_info', methods=['GET'])
def get_basic_info():
    return jsonify(basic_info)

@app.route('/basic_info_add', methods=['POST'])
def add_basic_info():
    data = request.get_json()
    basic_info.append(data)
    return jsonify({"message": "Basic info added successfully"})

@app.route('/basic_info_put/<int:index>', methods=['PUT'])
def update_basic_info(index):
    if index >= 0 and index < len(basic_info):
        data = request.get_json()
        basic_info[index] = data
        return jsonify({"message": "Basic info updated successfully"})
    else:
        return jsonify({"message": "Invalid index"})

@app.route('/basic_info_del/<int:index>', methods=['DELETE'])
def delete_basic_info(index):
    if index >= 0 and index < len(basic_info):
        del basic_info[index]
        return jsonify({"message": "Basic info deleted successfully"})
    else:
        return jsonify({"message": "Invalid index"})


def main():
    app.run(host="0.0.0.0", port=5200, debug=True)

if __name__ == '__main__':
    main()
