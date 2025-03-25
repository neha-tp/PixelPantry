import { useEffect, useState } from "react";
import { getNGOs } from "../api";

const NGOs = () => {
    const [ngos, setNgos] = useState([]);

    useEffect(() => {
        const fetchNGOs = async () => {
            try {
                const response = await getNGOs();
                setNgos(response.data.ngos);
            } catch (error) {
                console.error("Error fetching NGOs", error);
            }
        };
        fetchNGOs();
    }, []);

    return (
        <div className="container mt-4">
            <h2>Nearby NGOs</h2>
            <ul className="list-group">
                {ngos.map((ngo) => (
                    <li key={ngo._id} className="list-group-item">
                        <h5>{ngo.name}</h5>
                        <p>Contact: {ngo.contact}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default NGOs;
