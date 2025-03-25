import React, { useState, useEffect } from "react";
import axios from "axios";

function App() {
    const [posts, setPosts] = useState([]);
    const [newPost, setNewPost] = useState({ text: "", user_id: "", image: "" });
    const [comment, setComment] = useState({ post_id: "", user_id: "", comment: "" });

    useEffect(() => {
        fetchPosts();
    }, []);

    const fetchPosts = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:5000/posts");
            setPosts(response.data);
        } catch (error) {
            console.error("Error fetching posts:", error);
        }
    };

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setNewPost((prevPost) => ({ ...prevPost, image: reader.result.split(",")[1] })); 
            };
            reader.readAsDataURL(file);
        }
    };

    const createPost = async () => {
        try {
            await axios.post("http://127.0.0.1:5000/post", newPost, {
                headers: { "Content-Type": "application/json" },
            });
            setNewPost({ text: "", user_id: "", image: "" });
            fetchPosts();
        } catch (error) {
            console.error("Error creating post:", error.response ? error.response.data : error.message);
        }
    };

    const addComment = async () => {
        try {
            await axios.post("http://127.0.0.1:5000/comment", comment, {
                headers: { "Content-Type": "application/json" },
            });
            setComment({ post_id: "", user_id: "", comment: "" });
            fetchPosts();
        } catch (error) {
            console.error("Error adding comment:", error);
        }
    };

    return (
        <div>
            <h1>Community Forum</h1>

            <h2>Create a Post</h2>
            <input
                type="text"
                placeholder="Your User ID"
                value={newPost.user_id}
                onChange={(e) => setNewPost({ ...newPost, user_id: e.target.value })}
            />
            <textarea
                placeholder="Post text"
                value={newPost.text}
                onChange={(e) => setNewPost({ ...newPost, text: e.target.value })}
            />
            <input type="file" accept="image/*" onChange={handleImageUpload} />
            <button onClick={createPost}>Post</button>

            <h2>All Posts</h2>
            {posts.map((post) => (
                <div key={post.post_id} style={{ border: "1px solid black", padding: "10px", margin: "10px" }}>
                    <h3>{post.text}</h3>
                    {post.image_url && (
                        <img 
                            src={post.image_url} 
                            alt="Post" 
                            width="200" 
                            onError={(e) => { e.target.src = "fallback-image.png"; }}
                        />
                    )}
                    <p>Posted by: {post.user_id}</p>

                    <h4>Comments:</h4>
                    {post.comments.map((c, index) => (
                        <p key={index}><b>{c.user_id}:</b> {c.comment}</p>
                    ))}

                    <h4>Add a Comment</h4>
                    <input
                        type="text"
                        placeholder="Your User ID"
                        value={comment.user_id}
                        onChange={(e) => setComment({ ...comment, user_id: e.target.value, post_id: post.post_id })}
                    />
                    <input
                        type="text"
                        placeholder="Comment"
                        value={comment.comment}
                        onChange={(e) => setComment({ ...comment, comment: e.target.value })}
                    />
                    <button onClick={addComment}>Comment</button>
                </div>
            ))}
        </div>
    );
}

export default App;
