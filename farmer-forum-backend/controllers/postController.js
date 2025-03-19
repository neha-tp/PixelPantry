const Post = require("../models/Post");

// Create a Post
exports.createPost = async (req, res) => {
    const { user, text, location } = req.body;

    try {
        const post = new Post({
            user,
            text,
            location: { type: "Point", coordinates: location },
            image: req.file ? req.file.filename : null
        });

        await post.save();
        res.json(post);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
};

// Get Nearby Posts (within 50km)
exports.getNearbyPosts = async (req, res) => {
    const { lat, lng } = req.query;

    try {
        const posts = await Post.find({
            location: {
                $near: {
                    $geometry: { type: "Point", coordinates: [parseFloat(lng), parseFloat(lat)] },
                    $maxDistance: 50000 // 50km radius
                }
            }
        }).populate("user");

        res.json(posts);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
};
