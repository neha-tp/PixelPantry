import { useState } from "react";
import { getWeather, getAlerts } from "../api";

const WeatherAlerts = () => {
    const [location, setLocation] = useState("");
    const [weather, setWeather] = useState(null);
    const [alerts, setAlerts] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const fetchWeatherAndAlerts = async () => {
        if (!location) {
            setError("Please enter a location.");
            return;
        }
        
        setLoading(true);
        setError("");
        setWeather(null);
        setAlerts(null);

        try {
            const weatherResponse = await getWeather(location);
            setWeather(weatherResponse.data.data);

            const alertResponse = await getAlerts(location);
            setAlerts(alertResponse.data.alerts);
        } catch (err) {
            setError("Failed to fetch data. Please try again.");
            console.error("Error:", err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mt-4">
            <h2>Weather & Alerts</h2>

            <div className="input-group mb-3">
                <input
                    type="text"
                    className="form-control"
                    placeholder="Enter location"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                />
                <button className="btn btn-primary" onClick={fetchWeatherAndAlerts}>
                    Get Updates
                </button>
            </div>

            {loading && <p>Loading...</p>}
            {error && <p className="text-danger">{error}</p>}

            {weather && (
                <div className="card mt-3">
                    <div className="card-body">
                        <h5 className="card-title">{weather.name}</h5>
                        <p>Temperature: {weather.main.temp}°C</p>
                        <p>Condition: {weather.weather[0].description}</p>
                    </div>
                </div>
            )}

            {alerts && (
                <div className="alert alert-warning mt-3">
                    <h5>Weather Alerts</h5>
                    {Array.isArray(alerts) ? alerts.map((alert, i) => <p key={i}>{alert}</p>) : alerts}
                </div>
            )}
        </div>
    );
};

export default WeatherAlerts;
