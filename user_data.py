from pymongo import MongoClient

# MongoDB connection URI (replace with your MongoDB URI if you're using MongoDB Atlas or local instance)
uri = "mongodb://localhost:27017/"  # If using MongoDB Atlas, use the connection string provided there

# Connect to MongoDB
client = MongoClient(uri)

# Select the database and collection
db = client["Pixelpantry"]  # Database: Pixelpantry
user_collection = db["User"]  # Collection: user

# Sample farmer data to insert
farmers_data = [
    {"user_id": "user_001", "name" : "Shivam Kumar", "email": "shivam.kumar@farmer.in", "location": {"latitude": 28.7041, "longitude": 77.1025}, "weather_alerts": True, "ngo_notifications": False, "device_token": "token_001"},
    {"user_id": "user_002", "name" : "Anil Patel", "email": "anil.patel@farmer.in", "location": {"latitude": 23.0225, "longitude": 72.5714}, "weather_alerts": True, "ngo_notifications": True, "device_token": "token_002"},
    {"user_id": "user_003", "name" : "Vikram Singh", "email": "vikram.singh@farmer.in", "location": {"latitude": 26.8467, "longitude": 80.9462}, "weather_alerts": False, "ngo_notifications": False, "device_token": "token_003"},
    {"user_id": "user_004", "name" : "Pradeep K" , "email": "pradeep.k@farmer.in", "location": {"latitude": 19.0760, "longitude": 72.8777}, "weather_alerts": True, "ngo_notifications": True, "device_token": "token_004"},
    {"user_id": "user_005", "name" : "Rajesh R" , "email": "rajesh.r@farmer.in", "location": {"latitude": 15.2993, "longitude": 74.1240}, "weather_alerts": True, "ngo_notifications": False, "device_token": "token_005"},
    {"user_id": "user_006", "name" : "Neelam R" , "email": "neelam.r@farmer.in", "location": {"latitude": 28.6139, "longitude": 77.2090}, "weather_alerts": True, "ngo_notifications": True, "device_token": "token_006"},
    {"user_id": "user_007", "name" : "Gopal singh" , "email": "gopal.singh@farmer.in", "location": {"latitude": 21.1458, "longitude": 79.0882}, "weather_alerts": False, "ngo_notifications": False, "device_token": "token_007"},
    {"user_id": "user_008", "name" : "Sandeep D" , "email": "sandeep.d@farmer.in", "location": {"latitude": 30.7333, "longitude": 76.7794}, "weather_alerts": True, "ngo_notifications": False, "device_token": "token_008"},
    {"user_id": "user_009", "name" : "Amit K" , "email": "amit.k@farmer.in", "location": {"latitude": 22.5726, "longitude": 88.3639}, "weather_alerts": True, "ngo_notifications": True, "device_token": "token_009"},
    {"user_id": "user_010", "name" : "Manoj Yadav" , "email": "manoj.yadav@farmer.in", "location": {"latitude": 26.9124, "longitude": 75.7873}, "weather_alerts": False, "ngo_notifications": True, "device_token": "token_010"}
]

# Insert the farmer data into the 'user' collection
try:
    result = user_collection.insert_many(farmers_data)  # Insert multiple documents at once
    print(f"Successfully added {len(result.inserted_ids)} farmers to the database!")
except Exception as e:
    print(f"Error inserting data: {e}")
