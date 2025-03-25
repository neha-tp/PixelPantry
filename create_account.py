'''
from pymongo import MongoClient
from geopy.geocoders import Nominatim

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Change this if using MongoDB Atlas
db = client["Pixelpantry"]  # Database
user_collection = db["User"]  # Farmers collection
ngo_collection = db["Ngo"]  # NGO collection

# Function to get location coordinates using OpenStreetMap
def get_location(address):
    geolocator = Nominatim(user_agent="Pixel_Pantry")
    location = geolocator.geocode(address)
    if location:
        return {"latitude": location.latitude, "longitude": location.longitude}
    else:
        return None

# Ask user type
user_type = input("Are you a Farmer or an NGO? (Enter 'farmer' or 'ngo'): ").strip().lower()

if user_type == "farmer":
    user_id = input("Enter your User ID: ").strip()
    name = input("Enter your Name: ").strip()
    email = input("Enter your Email: ").strip()
    address = input("Enter your location (City, State, Country): ").strip()

    location = get_location(address)
    if not location:
        print("Invalid location. Please enter a correct address.")
    else:
        farmer_data = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "location": location
        }
        user_collection.insert_one(farmer_data)
        print("Farmer data inserted successfully!")

elif user_type == "ngo":
    ngo_id = input("Enter your NGO ID: ").strip()
    name = input("Enter NGO Name: ").strip()
    email = input("Enter NGO Email: ").strip()
    address = input("Enter NGO location (City, State, Country): ").strip()

    location = get_location(address)
    if not location:
        print("Invalid location. Please enter a correct address.")
    else:
        ngo_data = {
            "ngo_id": ngo_id,
            "name": name,
            "contact": email,
            "location": location
        }
        ngo_collection.insert_one(ngo_data)
        print("NGO data inserted successfully!")

else:
    print("Invalid selection. Please enter 'farmer' or 'ngo'.")
'''

from flask import Flask, request, jsonify
from pymongo import MongoClient
from geopy.geocoders import Nominatim
import bcrypt

app = Flask(__name__)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")  
db = client["Pixelpantry"]
user_collection = db["User"]
ngo_collection = db["Ngo"]

# Initialize Geolocator
geolocator = Nominatim(user_agent="Pixel_Pantry")

def get_coordinates(address):
    """Convert address to latitude & longitude using OpenStreetMap."""
    location = geolocator.geocode(address)
    if location:
        return {"latitude": location.latitude, "longitude": location.longitude}
    return None

def hash_password(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

@app.route("/register", methods=["POST"])
def register():
    """Register a farmer or an NGO."""
    data = request.json
    user_type = data.get("user_type", "").lower()
    password = data.get("password")
    print(password)
    if not password:
        return jsonify({"error": "Password is required"}), 400

    hashed_password = hash_password(password) , bcrypt.gensalt()  # Encrypt password
    print(hashed_password)
    if user_type == "farmer":
        user_data = {
            "user_id": data["user_id"],
            "name": data["name"],
            "email": data["email"],
            "password": hashed_password,  # Store encrypted password
            "location": get_coordinates(data["address"])
        }
        if not user_data["location"]:
            return jsonify({"error": "Invalid location"}), 400
        print(user_data)
        user_collection.insert_one(user_data)
        return jsonify({"message": "Farmer registered successfully!"})

    elif user_type == "ngo":
        ngo_data = {
            "ngo_id": data["ngo_id"],
            "name": data["name"],
            "contact": data["email"],
            "password": hashed_password,  # Store encrypted password
            "location": get_coordinates(data["address"])
        }
        if not ngo_data["location"]:
            return jsonify({"error": "Invalid location"}), 400
        
        ngo_collection.insert_one(ngo_data)
        return jsonify({"message": "NGO registered successfully!"})

    return jsonify({"error": "Invalid user type"}), 400

if __name__ == "__main__":
    app.run(debug=True)
