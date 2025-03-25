from flask import Flask, request, jsonify, send_from_directory
from pymongo import MongoClient
import uuid
import os
import base64
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["Pixelpantry"]
user_collection = db["User"]
post_collection = db["Posts"]

# Configure upload folder
# Configure upload folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/post", methods=["POST"])
def create_post():
    """Allow a registered user to create a post."""
    data = request.json
    user_id = data.get("user_id")
    text = data.get("text", "")
    image_data = data.get("image")

    # Check if user exists
    user = user_collection.find_one({"user_id": user_id})
    if not user:
        return jsonify({"error": "User not found"}), 404

    image_url = None
    if image_data:
        try:
            image_name = f"{uuid.uuid4()}.png"
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], image_name)

            # Decode Base64 and save the image
            with open(image_path, "wb") as img_file:
                img_file.write(base64.b64decode(image_data))

            image_url = f"http://127.0.0.1:5000/uploads/{image_name}"  # URL path for accessing
        except Exception as e:
            return jsonify({"error": f"Failed to save image: {str(e)}"}), 500

    post = {
        "post_id": str(uuid.uuid4()),  # Generate a unique post ID
        "user_id": user_id,
        "text": text,
        "image_url": image_url,
        "comments": []  # Empty list to store comments
    }
    post_collection.insert_one(post)
    post["_id"] = str(post_collection.inserted_id)  # Convert ObjectId to string
    return jsonify({"message": "Post created successfully!", "post": post})

@app.route("/posts", methods=["GET"])
def get_posts():
    """Fetch all posts and convert ObjectId to string."""
    posts = list(post_collection.find({}, {"_id": 1, "user_id": 1, "text": 1, "image_url": 1, "comments": 1}))
    
    for post in posts:
        if "_id" in post:  # Ensure '_id' exists before converting
            post["_id"] = str(post["_id"])
    
    return jsonify(posts)

@app.route("/comment", methods=["POST"])
def add_comment():
    """Allow users to comment on posts."""
    data = request.json
    post_id = data.get("post_id")
    user_id = data.get("user_id")
    comment_text = data.get("comment")

    post = post_collection.find_one({"post_id": post_id})
    if not post:
        return jsonify({"error": "Post not found"}), 404

    comment = {
        "user_id": user_id,
        "comment": comment_text
    }
    post_collection.update_one({"post_id": post_id}, {"$push": {"comments": comment}})
    return jsonify({"message": "Comment added!"})


# Serve uploaded images
@app.route("/uploads/<filename>")
def serve_image(filename):
    """Serve uploaded images."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
