const mongoose = require("mongoose");

const UserSchema = new mongoose.Schema({
    name: String,
    email: { type: String, unique: true },
    password: String,
    location: {
        type: { type: String, default: "Point" },
        coordinates: [Number] // [longitude, latitude]
    }
});

UserSchema.index({ location: "2dsphere" }); // Index for geospatial queries

module.exports = mongoose.model("User", UserSchema);
