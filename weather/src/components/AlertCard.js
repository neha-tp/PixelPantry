const AlertCard = ({ alerts }) => {
    if (!alerts) return null;

    return (
        <div className="alert alert-danger mt-3">
            <h5>Weather Alerts</h5>
            {Array.isArray(alerts) ? alerts.map((alert, i) => <p key={i}>{alert}</p>) : <p>{alerts}</p>}
        </div>
    );
};

export default AlertCard;
