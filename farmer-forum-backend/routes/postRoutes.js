const express = require("express");
const { createPost, getNearbyPosts } = require("../controllers/postController");
const upload = require("../middleware/uploadMiddleware");
const authMiddleware = require("../middleware/authMiddleware");

const router = express.Router();

router.post("/", authMiddleware, upload.single("image"), createPost); // Protected Route
router.get("/", getNearbyPosts);

module.exports = router;


