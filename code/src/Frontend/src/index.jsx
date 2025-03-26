import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import Navbar from "./components/NavBar/Navbar.jsx"; // Import Navbar
import Homepage from "./components/Homepage.jsx";
import About from "./components/About.jsx";
import RiskAnalysis from "./components/RiskAnalysis.jsx"

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <Navbar /> {/* Navbar is always visible */}
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/about" element={<About />} />
        <Route path="/risk-analysis" element={<RiskAnalysis />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
