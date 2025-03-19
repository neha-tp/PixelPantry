import { useState } from "react";
import { registerUser } from "../api";

const Register = () => {
    const [userData, setUserData] = useState({
        name: "",
        email: "",
        location: { latitude: "", longitude: "" },
        weather_alerts: true,
        ngo_notifications: true,
    });

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await registerUser(userData);
            alert("Registered successfully!");
        } catch (error) {
            console.error("Error registering user", error);
        }
    };

    return (
        <div className="container mt-4">
            <h2>Register as a Farmer</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" className="form-control mt-2" placeholder="Name" 
                    onChange={(e) => setUserData({ ...userData, name: e.target.value })} />
                <input type="email" className="form-control mt-2" placeholder="Email"
                    onChange={(e) => setUserData({ ...userData, email: e.target.value })} />
                <button className="btn btn-success mt-3">Register</button>
            </form>
        </div>
    );
};

export default Register;
