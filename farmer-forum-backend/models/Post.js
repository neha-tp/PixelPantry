const mongoose = require("mongoose");

const PostSchema = new mongoose.Schema({
    user: { type: mongoose.Schema.Types.ObjectId, ref: "User" },
    text: String,
    image: String,
    location: {
        type: { type: String, default: "Point" },
        coordinates: [Number] // [longitude, latitude]
    },
    createdAt: { type: Date, default: Date.now }
});

PostSchema.index({ location: "2dsphere" }); // Index for geospatial queries

module.exports = mongoose.model("Post", PostSchema);

