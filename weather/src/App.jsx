import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Home from "./Home";
import NewsPage from "./NewsPage";
//import FarmQuest from "./FarmQuest"; 
import ProfilePage from "./ProfilePage"; 
//import NgoList from "./components/NgoList"; 
import Chatbot from "./components/chatbot"; // ✅ Import Chatbot Component
import "./App.css"; 

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navigation Bar */}
        <header className="navbar">
          <h1 className="logo">Pixel Pantry</h1>
          <h2>Crop Guard</h2>
          <nav className="nav-links">
            <Link to="/">Home</Link>
            <Link to="/news">News</Link>
            
            <Link to="/profile">Profile</Link>
            
            
          </nav>
        </header>

        {/* Routes */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/news" element={<NewsPage />} />
          
          <Route path="/profile" element={<ProfilePage />} />
          
          
        </Routes>

        {/* Floating Chatbot Component (Accessible on All Pages) */}
        <Chatbot />

        {/* Footer */}
        <footer className="footer">
          <a href="#learn-more">Learn More</a>
        </footer>
      </div>
    </Router>
  );
}

export default App;
