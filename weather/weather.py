from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from pymongo import MongoClient
import requests
import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Thread
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

# Initialize Flask app
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSockets

# Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/"
app.config["MONGO_DBNAME"] = "Pixelpantry"
app.config["WEATHER_API_KEY"] = "c9fa254506b5415bf6efb8bc7e29757b"
app.config["WEATHER_API_URL"] = "http://api.openweathermap.org/data/2.5/weather"

# Initialize MongoDB
mongo_client = MongoClient(app.config["MONGO_URI"])
db = mongo_client[app.config["MONGO_DBNAME"]]

def get_weather(location):
    api_key = app.config["WEATHER_API_KEY"]
    url = app.config["WEATHER_API_URL"]
    params = {"q": location, "appid": api_key, "units": "metric"}
    response = requests.get(url, params=params)
    return response.json() if response.status_code == 200 else None

def check_abnormal_weather(weather_data):
    """ Checks for extreme weather conditions and returns alerts if any exist. """
    alerts = []

    if not weather_data or "main" not in weather_data:
        return None

    temp = weather_data["main"].get("temp", 0)
    weather_conditions = weather_data.get("weather", [])

    # Extreme temperature alerts
    if temp > 40:
        alerts.append("🔥 Extreme heat alert: Temperature above 40°C!")
    elif temp < 5:
        alerts.append("❄️ Extreme cold alert: Temperature below 5°C!")

    # Severe weather conditions
    for condition in weather_conditions:
        if "storm" in condition["main"].lower():
            alerts.append("🌩️ Severe storm alert: Thunderstorm detected!")
        elif "rain" in condition["main"].lower():
            alerts.append("🌧️ Heavy rain alert: Possible flooding! Do not use fertilizers and pesticides today")
        elif "snow" in condition["main"].lower():
            alerts.append("❄️ Heavy snowfall alert!")

    return alerts if alerts else None

def send_realtime_weather_updates():
    """ Fetches weather data and emits updates & alerts to the frontend. """
    while True:
        try:
            farmers = db.Users.find()
            for farmer in farmers:
                location = farmer.get("location")
                weather_data = get_weather(location)
                
                if weather_data:
                    # Send general weather updates
                    socketio.emit("weather_update", {"location": location, "weather": weather_data})

                    # Check for abnormal weather and send alerts
                    alerts = check_abnormal_weather(weather_data)
                    if alerts:
                        socketio.emit("weather_alert", {"location": location, "alerts": alerts})

            time.sleep(60)  # Fetch and send updates every 60 seconds
        except Exception as e:
            print(f"Error in real-time updates: {e}")

# Run WebSocket updates in a separate thread
update_thread = Thread(target=send_realtime_weather_updates)
update_thread.daemon = True
update_thread.start()

@app.route("/api/weather/<string:location>", methods=["GET"])
def weather(location):
    """ API endpoint to fetch weather manually. """
    weather_data = get_weather(location)
    if weather_data:
        return jsonify({"success": True, "data": weather_data}), 200
    return jsonify({"success": False, "error": "Weather data not found"}), 500

@app.route("/api/alert/<string:location>", methods=["GET"])
def alert(location):
    """ API endpoint to fetch weather alerts manually. """
    weather_data = get_weather(location)
    alerts = check_abnormal_weather(weather_data)
    
    if alerts:
        return jsonify({"success": True, "alerts": alerts}), 200
    return jsonify({"success": True, "alerts": "No active alerts"}), 200

'''
# Collection for forum posts
forum_collection = db["ForumPosts"]

# ------------------------- API Endpoints -------------------------

@app.route("/api/forum/post", methods=["POST"])
def create_forum_post():
    """ Allows farmers to create a forum post with text and optional image. """
    data = request.json
    user_id = data.get("user_id")
    content = data.get("content")
    image_url = data.get("image_url", None)  # Optional image URL
    location = data.get("location")

    if not user_id or not content or not location:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    post = {
        "user_id": user_id,
        "content": content,
        "image_url": image_url,
        "location": location,
        "timestamp": datetime.datetime.utcnow()
    }

    forum_collection.insert_one(post)
    return jsonify({"success": True, "message": "Post created successfully"}), 201


@app.route("/api/forum/posts", methods=["GET"])
def get_forum_posts():
    """ Fetches forum posts based on location coordinates. """
    lat = request.args.get("lat", type=float)
    lon = request.args.get("lon", type=float)
    if lat is None or lon is None:
        return jsonify({"success": False, "message": "Latitude and Longitude required"}), 400

    # Finding posts from nearby farmers (adjust radius as needed)
    nearby_posts = forum_collection.find({
        "location.latitude": {"$gte": lat - 0.5, "$lte": lat + 0.5},
        "location.longitude": {"$gte": lon - 0.5, "$lte": lon + 0.5}
    })

    posts = []
    for post in nearby_posts:
        posts.append({
            "user_id": post["user_id"],
            "content": post["content"],
            "image_url": post.get("image_url"),
            "location": post["location"],
            "timestamp": post["timestamp"].isoformat()
        })

    return jsonify({"success": True, "posts": posts}), 200'
'''

if __name__ == "__main__":
    socketio.run(app, debug=True)