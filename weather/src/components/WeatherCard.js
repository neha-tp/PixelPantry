const WeatherCard = ({ weather }) => {
    if (!weather) return null;

    return (
        <div className="card mt-3">
            <div className="card-body">
                <h5 className="card-title">{weather.name}</h5>
                <p>Temperature: {weather.main.temp}°C</p>
                <p>Condition: {weather.weather[0].description}</p>
            </div>
        </div>
    );
};

export default WeatherCard;
