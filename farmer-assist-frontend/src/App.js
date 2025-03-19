import { BrowserRouter, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import WeatherAlerts from "./pages/WeatherAlerts";

const App = () => (
    <BrowserRouter>
        <Navbar />
        <Routes>
            <Route path="/" element={<WeatherAlerts />} />
        </Routes>
    </BrowserRouter>
);

export default App;

