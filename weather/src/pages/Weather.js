import { useState } from "react";
import { getWeather } from "../api";
import WeatherCard from "../components/WeatherCard";

const Weather = () => {
    const [location, setLocation] = useState("");
    const [weather, setWeather] = useState(null);

    const fetchWeather = async () => {
        if (!location) return;
        try {
            const response = await getWeather(location);
            setWeather(response.data.data);
        } catch (error) {
            console.error("Error fetching weather", error);
        }
    };

    return (
        <div className="container mt-4">
            <h2>Weather Information</h2>
            <input type="text" className="form-control" placeholder="Enter location"
                value={location} onChange={(e) => setLocation(e.target.value)} />
            <button className="btn btn-primary mt-2" onClick={fetchWeather}>Get Weather</button>
            <WeatherCard weather={weather} />
        </div>
    );
};

export default Weather;
