import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

const Navbar = () => {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <div className="container">
                <Link className="navbar-brand" to="/">Farmer Assist</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav">
                        <li className="nav-item"><Link className="nav-link" to="/weather">Weather</Link></li>
                        <li className="nav-item"><Link className="nav-link" to="/alerts">Alerts</Link></li>
                        <li className="nav-item"><Link className="nav-link" to="/ngos">NGOs</Link></li>
                        <li className="nav-item"><Link className="nav-link" to="/register">Register</Link></li>
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
