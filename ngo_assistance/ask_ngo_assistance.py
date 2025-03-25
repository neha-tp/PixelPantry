'''
from pymongo import MongoClient
from geopy.geocoders import Nominatim
import os

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Adjust if using MongoDB Atlas
db = client["Pixelpantry"]
user_collection = db["User"]
ngo_collection = db["Ngo"]
assistance_collection = db["AssistanceRequests"]  # Collection to store messages

# Function to get city from coordinates using OpenStreetMap
def get_city_from_coordinates(lat, lon):
    geolocator = Nominatim(user_agent="Pixel_Pantry")
    location = geolocator.reverse((lat, lon), exactly_one=True)
    if location and 'address' in location.raw:
        return location.raw['address'].get('city', None)  # Extract city name
    return None

# Function to check nearby NGOs and send message
def send_assistance_request(user_id, message, image_path=None):
    # Fetch farmer details
    farmer = user_collection.find_one({"user_id": user_id})
    if not farmer:
        print("Farmer not found. Please check your User ID.")
        return

    farmer_location = farmer["location"]
    city = get_city_from_coordinates(farmer_location["latitude"], farmer_location["longitude"])
    farmer_lat, farmer_lon = farmer_location["latitude"], farmer_location["longitude"]

    print(f"DEBUG: Farmer's city detected as: {city}")  # Debugging line

    # Step 1: Find NGOs in the same city
    ngos_nearby = list(ngo_collection.find({"location.city": {"$regex": city, "$options": "i"}}))

    # Step 2: If no NGOs in the city, check for exact coordinates match
    if not ngos_nearby:
        print("No NGOs found in the same city. Checking for exact location match...")
        ngos_nearby = list(ngo_collection.find({
            "location.latitude": farmer_lat,
            "location.longitude": farmer_lon
        }))

    # Step 3: Send message if NGOs are found
    if ngos_nearby:
        assistance_request = {
            "user_id": user_id,
            "message": message,
            "image": image_path if image_path and os.path.exists(image_path) else None,
            "city": city,
            "ngos_contacted": [ngo["contact"] for ngo in ngos_nearby]
        }
        assistance_collection.insert_one(assistance_request)

        print(f"Message sent to {len(ngos_nearby)} NGOs in {city}")
        for ngo in ngos_nearby:
            print(f"✅ NGO Notified: {ngo['name']} ({ngo['contact']})")
    else:
        print("No NGOs found nearby. Try again later or contact support.")

# Example Usage
user_id = input("Enter your User ID: ").strip()
message = input("Describe your problem: ").strip()
image_path = input("Enter image path (optional, press Enter to skip): ").strip() or None

send_assistance_request(user_id, message, image_path)
'''

from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")  
db = client["Pixelpantry"]
user_collection = db["User"]
ngo_collection = db["Ngo"]
assistance_collection = db["AssistanceRequests"]

@app.route("/send_assistance", methods=["POST"])
def send_assistance():
    """Allow farmers to send text & image-based requests to NGOs."""
    data = request.form
    user_id = data.get("user_id")
    message = data.get("message")

    # Check if farmer exists
    farmer = user_collection.find_one({"user_id": user_id})
    if not farmer:
        return jsonify({"error": "Farmer not found"}), 404

    farmer_location = farmer["location"]

    # Find NGOs with same coordinates
    ngos_nearby = list(ngo_collection.find({
        "location.latitude": farmer_location["latitude"],
        "location.longitude": farmer_location["longitude"]
    }))

    # Store assistance request
    assistance_request = {
        "user_id": user_id,
        "message": message,
        "location": farmer_location,
        "ngos_contacted": [ngo["contact"] for ngo in ngos_nearby]
    }
    assistance_collection.insert_one(assistance_request)

    if ngos_nearby:
        return jsonify({"message": "Request sent!", "ngos": [ngo["name"] for ngo in ngos_nearby]})
    else:
        return jsonify({"message": "No NGOs found nearby"}), 404

@app.route("/ngo_messages/<ngo_id>", methods=["GET"])
def ngo_messages(ngo_id):
    """Allow NGOs to fetch assistance requests directed to them."""
    ngo = ngo_collection.find_one({"ngo_id": ngo_id})
    if not ngo:
        return jsonify({"error": "NGO not found"}), 404

    received_requests = list(assistance_collection.find({"ngos_contacted": ngo["contact"]}))
    
    return jsonify({"requests": received_requests})

if __name__ == "__main__":
    app.run(debug=True)
