import React, { useState } from "react";
import axios from "axios";

function AssistanceRequest() {
    const [userId, setUserId] = useState("");
    const [message, setMessage] = useState("");
    const [response, setResponse] = useState(null);

    const sendRequest = async () => {
        try {
            const formData = new FormData();
            formData.append("user_id", userId);
            formData.append("message", message);
            
            const res = await axios.post("http://localhost:5000/send_assistance", formData);
            setResponse(res.data);
        } catch (error) {
            setResponse(error.response ? error.response.data : { error: "Server error" });
        }
    };

    return (
        <div>
            <h2>Request Assistance</h2>
            <input 
                type="text" 
                placeholder="Enter User ID" 
                value={userId} 
                onChange={(e) => setUserId(e.target.value)} 
            />
            <textarea 
                placeholder="Describe your problem" 
                value={message} 
                onChange={(e) => setMessage(e.target.value)}
            />
            <button onClick={sendRequest}>Send Request</button>
            {response && <pre>{JSON.stringify(response, null, 2)}</pre>}
        </div>
    );
}

export default AssistanceRequest;
