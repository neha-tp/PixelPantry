import { useState } from "react";
import { getAlerts } from "../api";
import AlertCard from "../components/AlertCard";

const Alerts = () => {
    const [location, setLocation] = useState("");
    const [alerts, setAlerts] = useState(null);

    const fetchAlerts = async () => {
        if (!location) return;
        try {
            const response = await getAlerts(location);
            setAlerts(response.data.alerts);
        } catch (error) {
            console.error("Error fetching alerts", error);
        }
    };

    return (
        <div className="container mt-4">
            <h2>Weather Alerts</h2>
            <input type="text" className="form-control" placeholder="Enter location"
                value={location} onChange={(e) => setLocation(e.target.value)} />
            <button className="btn btn-warning mt-2" onClick={fetchAlerts}>Get Alerts</button>
            <AlertCard alerts={alerts} />
        </div>
    );
};

export default Alerts;
